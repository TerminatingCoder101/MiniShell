#!/usr/bin/env python3
import os, sys, subprocess, shlex, glob, tempfile
from google import genai

# ---------- Gemini setup ----------
try:
    client = genai.Client()
    HAS_GEMINI = True
except Exception:
    HAS_GEMINI = False

def ask_ai(prompt, model="gemini-2.5-flash"):
    if not HAS_GEMINI:
        return "ERROR: Gemini SDK not installed or GEMINI_API_KEY not set.\n"
    try:
        resp = client.models.generate_content(model=model, contents=[prompt])
        return resp.text
    except Exception as e:
        return f"AI error: {e}"

# ---------- Builtin Features ----------

def builtin_explain(cmd):
    return ask_ai(f"Explain what this shell command does:\n\n{cmd}")

def builtin_nl_command(nl):
    return ask_ai(f"Translate this natural language instruction into a Linux shell command and make it brief (no explanatations, just the command):\n\n{nl}")

def builtin_history_search(term):
    histfile = os.path.expanduser("~/.ai_shell_history")
    if not os.path.exists(histfile):
        return "No history yet.\n"
    with open(histfile) as f:
        lines = f.readlines()
    matches = [l.strip() for l in lines if term in l]
    if not matches:
        return "No matches found.\n"
    return "\n".join(matches)

def builtin_debug(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return ask_ai(f"I ran the command:\n{cmd}\nIt failed with error:\n{result.stderr}\nExplain the error and suggest a fix.")
    except Exception as e:
        return f"Error running debug: {e}"

def builtin_doc(path):
    if not os.path.exists(path):
        return f"File {path} not found."
    with open(path) as f:
        code = f.read()
    return ask_ai(f"Generate documentation/README for this code:\n\n{code}")

def builtin_hybrid(nl):
    cmd = ask_ai(f"Translate into a single Linux shell command only, no explanation:\n{nl}")
    return f"$ {cmd}"

def builtin_summarize_output(output):
    return ask_ai(f"Summarize the following shell output:\n\n{output}")

def builtin_plan(nl):
    return ask_ai(f"Translate this natural language task into a sequence of Linux shell commands:\n\n{nl}")

def builtin_fix(cmd, stderr):
    return ask_ai(f"I tried to run:\n{cmd}\nIt failed with error:\n{stderr}\nSuggest the correct fixed command.")

# ---------- Command Runner ----------

def run_command(cmd):
    # Feature: Explanation if ends with "?"
    if cmd.endswith("?"):
        return builtin_explain(cmd[:-1])

    # Feature: Natural language to shell
    if cmd.startswith("nl "):
        return builtin_nl_command(cmd[3:])

    # Feature: History search
    if cmd.startswith("history search "):
        return builtin_history_search(cmd.replace("history search ", ""))

    # Feature: Debug
    if cmd.startswith("debug "):
        return builtin_debug(cmd[6:])

    # Feature: Doc generator
    if cmd.startswith("doc "):
        return builtin_doc(cmd[4:])

    # Feature: Hybrid NL+shell
    if cmd.startswith("ai "):
        return builtin_hybrid(cmd[3:])

    # Feature: Summarize output
    if "| ai summarize" in cmd:
        parts = cmd.split("| ai summarize")
        try:
            result = subprocess.run(parts[0], shell=True, capture_output=True, text=True)
            return builtin_summarize_output(result.stdout)
        except Exception as e:
            return str(e)

    # Feature: Natural Planner
    if cmd.startswith("plan "):
        return builtin_plan(cmd[5:])

    # Feature: Direct Gemini Chat
    if cmd.startswith("gemini"):
        prompt = cmd[6:].strip()
        if not prompt:
            return "Enter something after 'gemini' to chat with Gemini."
        return ask_ai(prompt)

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return result.stdout
        else:
            fix = builtin_fix(cmd, result.stderr)
            return f"Error:\n{result.stderr}\nDid you mean:\n{fix}\n"
    except Exception as e:
        return str(e)

# ---------- Main Loop ----------

def main():
    histfile = os.path.expanduser("~/.ai_shell_history")
    os.makedirs(os.path.dirname(histfile), exist_ok=True)
    print("AI Shell ready. Type 'exit' to quit.")
    while True:
        try:
            cmd = input(">> ").strip()
            if not cmd:
                continue
            if cmd == "exit":
                break
            with open(histfile, "a") as f:
                f.write(cmd + "\n")
            output = run_command(cmd)
            if output:
                print(output)
        except (EOFError, KeyboardInterrupt):
            print("\nExiting shell.")
            break

if __name__ == "__main__":
    main()
