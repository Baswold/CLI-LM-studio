#!/bin/bash
# Bash completion for lms (CLI-LM-Studio)
#
# Installation:
#   1. Copy this file to /etc/bash_completion.d/lms
#   2. Or source it in your ~/.bashrc: source /path/to/shell-completion.bash
#   3. Reload your shell or run: source ~/.bashrc

_lms_completion() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"

    # Main commands
    local commands="chat models history config-show init --help --version --verbose"

    # chat subcommand options
    local chat_opts="--model -m --system -s --temperature -t --max-tokens --interactive -i --stream --no-stream --help"

    # models subcommand options
    local models_cmds="list info set-default"
    local models_list_opts="--detailed -d --help"
    local models_info_opts="--help"

    # history subcommand options
    local history_cmds="show search clear"
    local history_show_opts="--limit -n --all --help"
    local history_search_opts="--help"
    local history_clear_opts="--confirm -y --help"

    # Determine context
    case "${COMP_CWORD}" in
        1)
            # Complete main commands
            COMPREPLY=( $(compgen -W "${commands}" -- ${cur}) )
            return 0
            ;;
        2)
            # Complete subcommands based on main command
            case "${prev}" in
                models)
                    COMPREPLY=( $(compgen -W "${models_cmds}" -- ${cur}) )
                    return 0
                    ;;
                history)
                    COMPREPLY=( $(compgen -W "${history_cmds}" -- ${cur}) )
                    return 0
                    ;;
                chat)
                    COMPREPLY=( $(compgen -W "${chat_opts}" -- ${cur}) )
                    return 0
                    ;;
            esac
            ;;
        *)
            # Handle options for subcommands
            local main_cmd="${COMP_WORDS[1]}"
            local sub_cmd="${COMP_WORDS[2]}"

            case "${main_cmd}" in
                chat)
                    COMPREPLY=( $(compgen -W "${chat_opts}" -- ${cur}) )
                    return 0
                    ;;
                models)
                    case "${sub_cmd}" in
                        list)
                            COMPREPLY=( $(compgen -W "${models_list_opts}" -- ${cur}) )
                            return 0
                            ;;
                        info|set-default)
                            # TODO: Could autocomplete model names from 'lms models list'
                            COMPREPLY=()
                            return 0
                            ;;
                    esac
                    ;;
                history)
                    case "${sub_cmd}" in
                        show)
                            COMPREPLY=( $(compgen -W "${history_show_opts}" -- ${cur}) )
                            return 0
                            ;;
                        search)
                            COMPREPLY=( $(compgen -W "${history_search_opts}" -- ${cur}) )
                            return 0
                            ;;
                        clear)
                            COMPREPLY=( $(compgen -W "${history_clear_opts}" -- ${cur}) )
                            return 0
                            ;;
                    esac
                    ;;
            esac
            ;;
    esac
}

# Register completion function
complete -F _lms_completion lms
complete -F _lms_completion lmstudio
