#!/bin/bash


debug=1 #if debug is commented the programm work verbose


print(){

    message=$1 #first argument
    if [ -z $debug ];
        then
            return
    else
        echo "$message"
    fi
}


commit_and_push(){
        print "      cap[ f ] => Inner 'commit_and_push'";
        git add .
        read -p "        Commit comment: " comment
        git commit -q -m "$comment"
        git push -q
        print "      cap[ f ] => Pushed";
}

stash_commit(){
    git stash -q
    print "      sc [ f ] => Stashed";
    git pull -q
    git stash apply -q
    print "      sc [ f ] => Stash applied";
    commit_and_push
}

compare_and_commit(){
    rem="$(git log --remotes -1 --format=%ct )"
    loc="$(git log -1 --format=%ct )"
    if [ $rem -gt $loc ];
        then
            if [ -z "$(git status -s)" ];
            then
                print "    1[ > ] => Call commit_and_push"
                commit_and_push
            else
                print "    2[ > ] => Call stash_commit"
                stash_commit
            fi
    elif [ $rem -eq $loc ];
        then
            if [ -z "$(git status -s)" ];
                then
                    print "    3[ = ] => Pull ";
                    git pull -q
                    return

            else
                print "    4[ = ] => Call stash_commit"
                stash_commit
            fi
    else
        print "    5[ < ] => Call commit_and_push";
        commit_and_push
    fi
    return
}



compare_and_commit




# print  "you got it!!!!"

