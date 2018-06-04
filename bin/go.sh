#!/usr/bin/env bash

function run_statistics_word() {
    local unit=$1
    local min_doc_frequency=$2
    python -m bin.go --package bin.statistics.word --object WordDF  \
        --unit ${unit} \
        --min_doc_frequency ${min_doc_frequency}
}

function run_statistics() {
    run_statistics_word word 50
    run_statistics_word 1gram 50
    run_statistics_word 2gram 50
    run_statistics_word 3gram 50
}

function generate_feature_word_df() {
    local unit=$1
    local enable_set=$2
    local min_doc_frequency=$3

    local object_list=( WordDFEntropySum \
                        WordDFEntropyAverage \
                        WordDFProbabilitySum \
                        WordDFProbabilityAve \
                        WordDFProbabilityNorm \
                        WordDFProbabilitySumSum \
                        WordDFProbabilityAveSum)

    for object in ${object_list[@]}
    do
        python -m bin.go --package bin.feature.word --object ${object} \
            --unit ${unit} \
            --enable_set ${enable_set} \
            --min_doc_frequency ${min_doc_frequency}
    done
}

function generate_feature() {
    generate_feature_word_df word true 50
    generate_feature_word_df word false 50

    generate_feature_word_df 1gram true 50
    generate_feature_word_df 1gram false 50

    generate_feature_word_df 2gram true 50
    generate_feature_word_df 2gram false 50

    generate_feature_word_df 3gram true 50
    generate_feature_word_df 3gram false 50
}

run_statistics
generate_feature