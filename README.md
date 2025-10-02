```markdown
# AI Mini Shell

An intelligent shell augmentation leveraging Google Gemini to provide AI-powered features directly within your command-line interface. This script enhances your shell experience by integrating AI capabilities for command explanation, natural language command generation, debugging, output summarization, and more.

## Features

The AI Mini Shell extends your standard command-line usage with the following intelligent functionalities:

*   **Explain Commands (`<command>?`)**: Get a natural language explanation of what a shell command does.
    *   Example: `ls -l?`

*   **Natural Language to Command (`nl <instruction>`)**: Translate a natural language instruction into a Linux shell command.
    *   Example: `nl list all python files in the current directory`

*   **History Search (`history search <term>`)**: Search through your AI Mini Shell command history for a specific term.
    *   Example: `history search git`

*   **Debug Command Output (`debug <command>`)**: Run a command and if it fails, get an AI explanation of the error and a suggested fix.
    *   Example: `debug cat /nonexistent_file`

*   **Generate Code Documentation (`doc <filepath>`)**: Provide a file path, and the AI will generate documentation or a README for its content.
    *   Example: `doc my_script.py`

*   **Hybrid NL-to-Shell Command (`ai <instruction>`)**: Translate a natural language instruction into a single Linux shell command and print it, allowing you to copy/paste or review.
    *   Example: `ai create a temporary directory`

*   **Summarize Command Output (`<command> | ai summarize`)**: Pipe the output of any command into `ai summarize` to get a concise summary of the results.
    *   Example: `ls -l | ai summarize`

*   **Natural Language Planner (`plan <task>`)**: Describe a complex task in natural language, and the AI will generate a sequence of Linux shell commands to accomplish it.
    *   Example: `plan setup a python virtual environment and install requests`

*   **Automatic Command Fixer (on error)**: If a regular shell command (not one of the special AI commands) fails, the AI will automatically suggest a corrected command based on the error output.

*   **Direct Gemini Chat (`gemini <prompt>`)**: Engage directly with the Gemini model for any general query or conversation.
    *   Example: `gemini What is the capital of France?`

## Installation

1.  **Save the script**: Save the provided Python code as a file, for example, `ai_shell.py`.
2.  **Make it executable**:
    ```bash
    chmod +x ai_shell.py
    ```
3.  **Install dependencies**:
    ```bash
    pip install google-generativeai
    ```

## Configuration

### Google Gemini API Key

This shell relies on the Google Gemini API. You need to obtain an API key and make it available to the script.

1.  **Get an API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey) and generate a new API key.
2.  **Set Environment Variable**: Set the `GEMINI_API_KEY` environment variable in your shell profile (e.g., `~/.bashrc`, `~/.zshrc`) or before running the script.

    ```bash
    echo 'export GEMINI_API_KEY="YOUR_API_KEY_HERE"' >> ~/.bashrc # or ~/.zshrc
    source ~/.bashrc # or source ~/.zshrc
    ```
    **Replace `YOUR_API_KEY_HERE` with your actual API key.**

    **Note:** If `GEMINI_API_KEY` is not set or the `google-generativeai` SDK is not installed, the AI features will return an error message.

## Usage

1.  **Start the AI Mini Shell**:
    ```bash
    ./mini_shell.py
    ```
    You will see a prompt: `>> `.

2.  **Execute commands**: Type any standard Linux command or use one of the AI-powered features.

    ```bash
    >> ls -l
    total 4
    -rwxr-xr-x 1 user user 3878 May  1 10:00 ai_shell.py

    >> ls -l?
    The `ls -l` command lists files in the current directory in a long format, showing detailed information such as permissions, number of hard links, owner, group, size, and modification time.

    >> nl how much disk space is left?
    df -h

    >> df -h
    Filesystem      Size  Used Avail Use% Mounted on
    udev            3.9G     0  3.9G   0% /dev
    tmpfs           797M  1.7M  795M   1% /run
    /dev/sda2        49G   14G   33G  30% /
    tmpfs           3.9G     0  3.9G   0% /dev/shm
    tmpfs           5.0M  4.0K  5.0M   1% /run/lock
    tmpfs           3.9G     0  3.9G   0% /sys/fs/cgroup
    /dev/sda1       511M  5.3M  506M   2% /boot/efi
    tmpfs           797M   24K  797M   1% /run/user/1000

    >> cat /nonexistent_file
    Error:
    cat: /nonexistent_file: No such file or directory
    Did you mean:
    To check if a file exists, you can use `[ -f /nonexistent_file ] && echo "File exists" || echo "File does not exist"`.
    If you intended to create or write to a file, consider `echo "content" > /nonexistent_file`.
    If you meant a different file, please provide the correct path.

    >> debug cat /nonexistent_file
    The command `cat /nonexistent_file` failed because the file `/nonexistent_file` does not exist.
    To fix this, ensure the file path is correct or create the file before attempting to read it.
    For example, to create an empty file: `touch /nonexistent_file`
    Or to create it with some content: `echo "Hello" > /nonexistent_file`

    >> plan find all .txt files and count their lines
    Here's a plan to find all .txt files and count their lines:

    1.  **Find .txt files:** Use `find . -name "*.txt"` to locate all files ending with `.txt` in the current directory and its subdirectories.
    2.  **Count lines for each file:** Use `xargs wc -l` to pass each found file to the `wc -l` command, which counts lines.

    Combined command:
    `find . -name "*.txt" -print0 | xargs -0 wc -l`

    >> gemini What is the capital of France?
    The capital of France is Paris.

    >> exit
    Exiting shell.
    ```

## History Management

The AI Mini Shell automatically records all commands you type into a history file located at `~/.ai_shell_history`. You can search this history using the `history search <term>` command.

## AI Model

By default, the shell uses the `gemini-2.5-flash` model for AI interactions.

## Disclaimer

*   **API Costs**: Be aware that using the Gemini API may incur costs depending on your usage and Google's pricing policy.
*   **AI Accuracy**: AI-generated responses can sometimes be inaccurate, incomplete, or suggest commands that are not entirely optimal or safe. Always review AI suggestions before executing them, especially for commands that modify your system or data.
*   **Security**: Do not expose your `GEMINI_API_KEY` publicly. Keep it secure as you would with any sensitive credential.
```
