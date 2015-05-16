#!/bin/bash 
Nf=`ls ../XMLdata/failing/*.plist | wc -w`
Ns=`ls ../XMLdata/passing/*.plist | wc -w`
Ncf=0
Ncs=0
Nuf=0
reg='TOTAL +([0-9]+) +([0-9]+) +([0-9]+)%'
function single_test()
{
    local res=$2
    local f=$1
    coverage run xpcmd.py $f &> /dev/null
    report=`coverage report`
    while read -r line; do
        if [[ $line =~ $reg ]]
        then
            break
        fi
    done <<< $report
    eval $res='("${BASH_REMATCH[@]}")'
}
function test_type()
{
    local t=$1
    local stmts=0
    local miss=0
    local res1=$2
    local res2=$3 
    local -a record
    for f in `ls ../XMLdata/$t/*.plist`
    do
        single_test $f record
        stmts=`echo "$stmts + ${record[1]}" | bc`
        miss=`echo "$miss + ${record[2]}" | bc`
    done
    eval $res1='"$stmts"'
    eval $res2='"$miss"'
}
function metric1_Tarantula()
{
    echo "scale=4; ($Ncf/$Nf)/(($Ncf/$Nf)+($Ncs/$Ns))" | bc
}
function metric2_Ochiai()
{
    echo "scale=4; $Ncf/sqrt($Nf*($Ncf+$Ncs))" | bc
}
function metric3_Ochiai()
{
    echo "scale=4; $Ncf-$Ncs/($Ns+1)" | bc
}
function main()
{
    local cover_total_stmts_pass=0
    local miss_total_stmts_pass=0
    test_type passing cover_total_stmts_pass miss_total_stmts_pass
    local cover_total_stmts_fail=0
    local miss_total_stmts_fail=0
    test_type failing cover_total_stmts_fail miss_total_stmts_fail
    Ncf=$cover_total_stmts_fail
    Nuf=$miss_total_stmts_fail
    Ncs=$cover_total_stmts_pass
    #Nus=$miss_total_stmts_pass
    #echo $Ncf $Nuf $Ncs
    metric1_Tarantula
    metric2_Ochiai
    metric3_Ochiai

}
#start
main
#finish
