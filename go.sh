#!/usr/bin/env bash

function run_statistics_word() {
    local conf_path=$1

    local unit=$2
    local min_doc_frequency=$3

    python -m bin.go --package bin.statistics.word \
        --conf ${conf_path} \
        --object WordDF  \
        --unit ${unit} \
        --min_doc_frequency ${min_doc_frequency}
}

function run_statistics() {
    local conf_path=$1

    run_statistics_word ${conf_path} word 50
    run_statistics_word ${conf_path} 1gram 50
    run_statistics_word ${conf_path} 2gram 50
    run_statistics_word ${conf_path} 3gram 50
    run_statistics_word ${conf_path} 4gram 50
}

function generate_feature_word_df() {
    local conf_path=$1

    local unit=$2
    local enable_set=$3
    local min_doc_frequency=$4

    local object_list=( WordDFEntropySum \
                        WordDFEntropyAverage \
                        WordDFProbabilitySum \
                        WordDFProbabilityAve \
                        WordDFProbabilityNorm \
                        WordDFProbabilitySumSum \
                        WordDFProbabilityAveSum)

    for object in ${object_list[@]}
    do
        python -m bin.go --package bin.feature.word \
            --conf ${conf_path} \
            --object ${object} \
            --unit ${unit} \
            --enable_set ${enable_set} \
            --min_doc_frequency ${min_doc_frequency}
    done
}

function generate_feature() {
    local conf_path=$1

    generate_feature_word_df ${conf_path} word true 50
    generate_feature_word_df ${conf_path} word false 50

    generate_feature_word_df ${conf_path} 1gram true 50
    generate_feature_word_df ${conf_path} 1gram false 50

    generate_feature_word_df ${conf_path} 2gram true 50
    generate_feature_word_df ${conf_path} 2gram false 50

    generate_feature_word_df ${conf_path} 3gram true 50
    generate_feature_word_df ${conf_path} 3gram false 50

    generate_feature_word_df ${conf_path} 4gram true 50
    generate_feature_word_df ${conf_path} 4gram false 50
}

conf_path=$1
run_statistics ${conf_path}
generate_feature ${conf_path}