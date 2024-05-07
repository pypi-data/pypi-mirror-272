function GetOciTopLevelCommand_opensearch() {
    return 'opensearch'
}

function GetOciSubcommands_opensearch() {
    $ociSubcommands = @{
        'opensearch' = 'backup cluster'
        'opensearch backup' = 'delete get list update'
        'opensearch cluster' = 'backup create delete get list list-versions resizehorizontal resizevertical restore update work-request work-request-error work-request-log-entry'
        'opensearch cluster work-request' = 'get list'
        'opensearch cluster work-request-error' = 'list'
        'opensearch cluster work-request-log-entry' = 'list'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_opensearch() {
    $ociCommandsToLongParams = @{
        'opensearch backup delete' = 'force from-json help if-match max-wait-seconds opensearch-cluster-backup-id wait-for-state wait-interval-seconds'
        'opensearch backup get' = 'from-json help opensearch-cluster-backup-id'
        'opensearch backup list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order source-opensearch-cluster-id'
        'opensearch backup update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds opensearch-cluster-backup-id wait-for-state wait-interval-seconds'
        'opensearch cluster backup' = 'compartment-id display-name from-json help if-match max-wait-seconds opensearch-cluster-id wait-for-state wait-interval-seconds'
        'opensearch cluster create' = 'compartment-id data-node-count data-node-host-bare-metal-shape data-node-host-memory-gb data-node-host-ocpu-count data-node-host-type data-node-storage-gb defined-tags display-name freeform-tags from-json help master-node-count master-node-host-bare-metal-shape master-node-host-memory-gb master-node-host-ocpu-count master-node-host-type max-wait-seconds opendashboard-node-count opendashboard-node-host-memory-gb opendashboard-node-host-ocpu-count security-master-user-name security-master-user-password-hash security-mode software-version subnet-compartment-id subnet-id system-tags vcn-compartment-id vcn-id wait-for-state wait-interval-seconds'
        'opensearch cluster delete' = 'force from-json help if-match max-wait-seconds opensearch-cluster-id wait-for-state wait-interval-seconds'
        'opensearch cluster get' = 'from-json help opensearch-cluster-id'
        'opensearch cluster list' = 'all compartment-id display-name from-json help id lifecycle-state limit page page-size sort-by sort-order'
        'opensearch cluster list-versions' = 'all compartment-id from-json help limit page page-size'
        'opensearch cluster resizehorizontal' = 'data-node-count defined-tags freeform-tags from-json help if-match master-node-count max-wait-seconds opendashboard-node-count opensearch-cluster-id wait-for-state wait-interval-seconds'
        'opensearch cluster resizevertical' = 'data-node-host-memory-gb data-node-host-ocpu-count data-node-storage-gb defined-tags freeform-tags from-json help if-match master-node-host-memory-gb master-node-host-ocpu-count max-wait-seconds opendashboard-node-host-memory-gb opendashboard-node-host-ocpu-count opensearch-cluster-id wait-for-state wait-interval-seconds'
        'opensearch cluster restore' = 'compartment-id from-json help if-match max-wait-seconds opensearch-cluster-backup-id opensearch-cluster-id prefix wait-for-state wait-interval-seconds'
        'opensearch cluster update' = 'defined-tags display-name force freeform-tags from-json help if-match max-wait-seconds opensearch-cluster-id security-master-user-name security-master-user-password-hash security-mode software-version wait-for-state wait-interval-seconds'
        'opensearch cluster work-request get' = 'from-json help work-request-id'
        'opensearch cluster work-request list' = 'all compartment-id from-json help limit page page-size source-resource-id work-request-id'
        'opensearch cluster work-request-error list' = 'all from-json help limit page page-size work-request-id'
        'opensearch cluster work-request-log-entry list' = 'all from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_opensearch() {
    $ociCommandsToShortParams = @{
        'opensearch backup delete' = '? h'
        'opensearch backup get' = '? h'
        'opensearch backup list' = '? c h'
        'opensearch backup update' = '? h'
        'opensearch cluster backup' = '? c h'
        'opensearch cluster create' = '? c h'
        'opensearch cluster delete' = '? h'
        'opensearch cluster get' = '? h'
        'opensearch cluster list' = '? c h'
        'opensearch cluster list-versions' = '? c h'
        'opensearch cluster resizehorizontal' = '? h'
        'opensearch cluster resizevertical' = '? h'
        'opensearch cluster restore' = '? c h'
        'opensearch cluster update' = '? h'
        'opensearch cluster work-request get' = '? h'
        'opensearch cluster work-request list' = '? c h'
        'opensearch cluster work-request-error list' = '? h'
        'opensearch cluster work-request-log-entry list' = '? h'
    }
    return $ociCommandsToShortParams
}