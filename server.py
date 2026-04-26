#!/usr/bin/env python3
"""
Skill Lifecycle HTTP Server
Serves the dashboard + provides edit API that creates GitHub PRs.
"""
import http.server
import json
import os
import subprocess
import re
import urllib.parse
from datetime import datetime
from pathlib import Path

# Configuration
PORT = 9099
WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
SKILL_DIRS = [
    os.path.join(WORKSPACE, ".agents", "skills"),
    os.path.join(WORKSPACE, "skills"),
]
REPO_DIR = os.path.join(WORKSPACE, "skill-lifecycle")
GIT_USER = "Rick (via OpenClaw)"
GIT_EMAIL = "rick@peakpeak.ai"

class SkillAPIHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        # API endpoints
        if path == "/api/skills":
            self.send_json_response(self.get_all_skills())
            return
        elif path == "/api/skill-content":
            params = urllib.parse.parse_qs(parsed.query)
            name = params.get("name", [None])[0]
            if name:
                content = self.get_skill_content(name)
                if content is not None:
                    self.send_json_response({"name": name, "content": content})
                else:
                    self.send_json_response({"error": "Skill not found"}, 404)
            else:
                self.send_json_response({"error": "Missing 'name' parameter"}, 400)
            return
        
        # Serve static files
        return super().do_GET()
    
    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        
        if path == "/api/save-skill":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body.decode("utf-8"))
            result = self.save_skill_and_create_pr(data)
            self.send_json_response(result)
            return
        
        self.send_json_response({"error": "Not found"}, 404)
    
    # ── Helpers ──
    
    def send_json_response(self, data, status=200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)
    
    def get_all_skills(self):
        """Return all skills from workspace directories + registry"""
        skills = {}
        for skills_dir in SKILL_DIRS:
            if not os.path.isdir(skills_dir):
                continue
            for name in os.listdir(skills_dir):
                skill_path = os.path.join(skills_dir, name)
                sk_path = os.path.join(skill_path, "SKILL.md")
                if os.path.isdir(skill_path) and os.path.isfile(sk_path):
                    # Try to read frontmatter
                    desc = ""
                    try:
                        with open(sk_path) as f:
                            content = f.read()
                        m = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
                        if m:
                            import yaml
                            try:
                                meta = yaml.safe_load(m.group(1))
                                if meta:
                                    desc = meta.get("description", "")
                            except:
                                pass
                    except:
                        pass
                    skills[name] = {
                        "name": name,
                        "description": desc[:100] if desc else "",
                        "path": skill_path,
                        "size": os.path.getsize(sk_path) if os.path.isfile(sk_path) else 0,
                        "stage": self.get_lifecycle_stage(name),
                    }
        return skills
    
    def get_lifecycle_stage(self, name):
        """Read lifecycle stage from registry"""
        registry_path = os.path.join(REPO_DIR, "skills-registry.json")
        try:
            with open(registry_path) as f:
                registry = json.load(f)
            return registry.get("skills", {}).get(name, {}).get("stage", "—")
        except:
            return "—"
    
    def get_skill_content(self, name):
        """Return the full SKILL.md content for a skill"""
        for skills_dir in SKILL_DIRS:
            sk_path = os.path.join(skills_dir, name, "SKILL.md")
            if os.path.isfile(sk_path):
                try:
                    with open(sk_path) as f:
                        return f.read()
                except:
                    return None
        return None
    
    def save_skill_and_create_pr(self, data):
        """
        Save a skill's SKILL.md, commit to a branch, and create a PR.
        
        Expected POST body:
        {
            "name": "skill-name",
            "content": "full SKILL.md content",
            "message": "Optional commit message"
        }
        """
        name = data.get("name", "").strip()
        content = data.get("content", "").strip()
        message = data.get("message", "").strip() or f"Edit {name}: update SKILL.md"
        
        if not name or not content:
            return {"success": False, "error": "Missing 'name' or 'content'"}
        
        # Find the skill in workspace
        skill_dir = None
        for skills_dir in SKILL_DIRS:
            candidate = os.path.join(skills_dir, name)
            if os.path.isdir(candidate) and os.path.isfile(os.path.join(candidate, "SKILL.md")):
                skill_dir = candidate
                break
        
        if not skill_dir:
            return {"success": False, "error": f"Skill '{name}' not found"}
        
        target_path = os.path.join(skill_dir, "SKILL.md")
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        branch = f"edit/{name}/{timestamp}"
        
        try:
            if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
                return {"success": False, "error": "Repo not initialized in skill-lifecycle"}
            
            def git(args):
                return subprocess.run(
                    ["git"] + args,
                    cwd=REPO_DIR, capture_output=True, text=True, timeout=30,
                    env={**os.environ,
                         "GIT_AUTHOR_NAME": GIT_USER, "GIT_AUTHOR_EMAIL": GIT_EMAIL,
                         "GIT_COMMITTER_NAME": GIT_USER, "GIT_COMMITTER_EMAIL": GIT_EMAIL}
                )
            
            # 1. Create branch from main
            r = git(["checkout", "main"])
            if r.returncode != 0 and "did not match any file" in r.stderr:
                return {"success": False, "error": f"Repo issue: {r.stderr.strip()}"}
            
            r = git(["checkout", "-b", branch])
            if r.returncode != 0:
                return {"success": False, "error": f"Branch creation failed: {r.stderr.strip()}"}
            
            # 2. Write to BOTH locations:
            #    a) .agents/skills/<name>/SKILL.md — live OpenClaw location
            #    b) skills/<name>/SKILL.md — in the repo for git tracking
            
            with open(target_path, "w") as f:
                f.write(content)
            
            repo_skill_path = os.path.join(REPO_DIR, "skills", name, "SKILL.md")
            os.makedirs(os.path.dirname(repo_skill_path), exist_ok=True)
            with open(repo_skill_path, "w") as f:
                f.write(content)
            
            # 3. Commit in the repo
            relative_repo_path = os.path.join("skills", name, "SKILL.md")
            r = git(["add", relative_repo_path])
            if r.returncode != 0:
                git(["checkout", "main"])
                git(["branch", "-D", branch])
                return {"success": False, "error": f"git add failed: {r.stderr.strip()}"}
            
            r = git(["commit", "-m", message])
            if r.returncode != 0:
                git(["checkout", "main"])
                git(["branch", "-D", branch])
                return {"success": False, "error": f"git commit failed: {r.stderr.strip()}"}
            
            # 4. Push branch
            r = git(["push", "-u", "origin", branch])
            if r.returncode != 0:
                return {"success": False, "error": f"git push failed: {r.stderr.strip()}"}
            
            # 5. Create PR
            pr_body = (
                f"## Changes\n\n"
                f"Edited `{relative_repo_path}` via the Skill Lifecycle Dashboard.\n\n"
                f"**Commit message:** {message}\n\n"
                f"---\n_Automated by Rick (OpenClaw)_"
            )
            r = subprocess.run(
                ["gh", "pr", "create", "--repo", "michaldanilczyk-ops/rick-skills",
                 "--title", f"Edit {name}: {message}",
                 "--body", pr_body,
                 "--base", "main", "--head", branch],
                capture_output=True, text=True, timeout=30
            )
            if r.returncode != 0:
                return {"success": False, "error": f"PR creation failed: {r.stderr.strip()}", "branch": branch}
            
            pr_url = r.stdout.strip()
            
            # 6. Switch back to main
            git(["checkout", "main"])
            
            return {
                "success": True,
                "pr_url": pr_url,
                "branch": branch,
                "message": f"PR created: {pr_url}",
                "relative_path": relative_repo_path,
            }
            
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Git operation timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    # Check repo setup
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        print(f"WARNING: No git repo at {REPO_DIR}")
        print("Run: cd ~/.openclaw/workspace/skill-lifecycle && git init && git add -A && git commit -m 'init'")
    
    server_address = ("", PORT)
    httpd = http.server.HTTPServer(server_address, SkillAPIHandler)
    print(f"🚀 Skill Lifecycle Server running on http://0.0.0.0:{PORT}")
    print(f"   Dashboard: http://localhost:{PORT}/dashboard.html")
    print(f"   API:       http://localhost:{PORT}/api/skills")
    print(f"   GitHub:    https://github.com/michaldanilczyk-ops/rick-skills")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        httpd.shutdown()
