# Provides a platform-portable version of realpath that works on MacOS
# Taken from: https://stackoverflow.com/a/61750453

_realpath() {

    # GNU realpath replacement for bash 3.2 (OS X)
    # accepts --relative-to= and --relative-base options
    # and produces canonical (relative or absolute) paths for each
    # argument on stdout, errors on stderr, and returns 0 on success
    # and 1 if at least 1 path triggered an error.

    local relative_to relative_base seenerr path

    relative_to=
    relative_base=
    seenerr=

    while [[ $# -gt 0 ]]; do
        case $1 in
            "--relative-to="*)
                relative_to=$(_canonicalize_filename_mode "${1#*=}")
                shift 1;;
            "--relative-base="*)
                relative_base=$(_canonicalize_filename_mode "${1#*=}")
                shift 1;;
            *)
                break;;
        esac
    done

    if [[
        -n $relative_to
        && -n $relative_base
        && ${relative_to#${relative_base}/} == "$relative_to"
    ]]; then
        # relative_to is not a subdir of relative_base -> ignore both
        relative_to=
        relative_base=
    elif [[ -z $relative_to && -n $relative_base ]]; then
        # if relative_to has not been set but relative_base has, then
        # set relative_to from relative_base, simplifies logic later on
        relative_to="$relative_base"
    fi

    for path in "$@"; do
        if ! real=$(_canonicalize_filename_mode "$path"); then
            seenerr=1
            continue
        fi

        # make path relative if so required
        if [[
            -n $relative_to
            && ( # path must not be outside relative_base to be made relative
                -z $relative_base || ${real#${relative_base}/} != "$real"
            )
        ]]; then
            local common_part parentrefs

            common_part="$relative_to"
            parentrefs=
            while [[ ${real#${common_part}/} == "$real" ]]; do
                common_part="$(dirname "$common_part")"
                parentrefs="..${parentrefs:+/$parentrefs}"
            done

            if [[ $common_part != "/" ]]; then
                real="${parentrefs:+${parentrefs}/}${real#${common_part}/}"
            fi
        fi

        echo "$real"
    done
    if [[ $seenerr ]]; then
        return 1
    fi
}

if ! command -v realpath > /dev/null 2>&1; then
    # realpath is not available on OSX unless you install the `coreutils` brew
    realpath() { _realpath "$@"; }
fi

