#!/usr/bin/fish

set repo_path /tmp/repo
set base_branch develop

git config --global advice.detachedHead false

function checkout_commit
    git checkout $argv >/dev/null 2>&1
end

function get_hash_history
    git log --format="%H"
end

function create_tmp_copy
    echo "copying repo contents to $repo_path"
    rm -rf $repo_path
    git clone /repo $repo_path
end

function analyse
    github-linguist
end

create_tmp_copy
cd $repo_path

for hash in (get_hash_history)
    checkout_commit $hash
    analyse | tr "\n" ";" | xargs -0 printf "$hash;%s\n"
end
