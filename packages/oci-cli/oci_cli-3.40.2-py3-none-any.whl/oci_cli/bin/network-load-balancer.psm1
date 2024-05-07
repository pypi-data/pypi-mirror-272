function GetOciTopLevelCommand_network_load_balancer() {
    return 'network-load-balancer'
}

function GetOciSubcommands_network_load_balancer() {
    $ociSubcommands = @{
        'network-load-balancer' = 'backend backend-health backend-set backend-set-health backend-set-summary backend-summary health-checker listener listener-protocols listener-summary network-load-balancer network-load-balancer-health network-load-balancing-policy work-request work-request-error work-request-log-entry'
        'network-load-balancer backend' = 'create delete get update'
        'network-load-balancer backend-health' = 'get'
        'network-load-balancer backend-set' = 'create delete get update'
        'network-load-balancer backend-set-health' = 'get'
        'network-load-balancer backend-set-summary' = 'list-backend-sets'
        'network-load-balancer backend-summary' = 'list-backends'
        'network-load-balancer health-checker' = 'get update'
        'network-load-balancer listener' = 'create delete get update'
        'network-load-balancer listener-protocols' = 'list-network-load-balancers-protocols'
        'network-load-balancer listener-summary' = 'list-listeners'
        'network-load-balancer network-load-balancer' = 'change-compartment create delete get list update update-network-security-groups'
        'network-load-balancer network-load-balancer-health' = 'get list'
        'network-load-balancer network-load-balancing-policy' = 'list-network-load-balancers-policies'
        'network-load-balancer work-request' = 'get list'
        'network-load-balancer work-request-error' = 'list'
        'network-load-balancer work-request-log-entry' = 'list-work-request-logs'
    }
    return $ociSubcommands
}

function GetOciCommandsToLongParams_network_load_balancer() {
    $ociCommandsToLongParams = @{
        'network-load-balancer backend create' = 'backend-set-name from-json help if-match ip-address is-backup is-drain is-offline max-wait-seconds name network-load-balancer-id port target-id wait-for-state wait-interval-seconds weight'
        'network-load-balancer backend delete' = 'backend-name backend-set-name force from-json help if-match max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer backend get' = 'backend-name backend-set-name from-json help if-none-match network-load-balancer-id'
        'network-load-balancer backend update' = 'backend-name backend-set-name from-json help if-match is-backup is-drain is-offline max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds weight'
        'network-load-balancer backend-health get' = 'backend-name backend-set-name from-json help network-load-balancer-id'
        'network-load-balancer backend-set create' = 'backends from-json health-checker help if-match is-preserve-source max-wait-seconds name network-load-balancer-id policy wait-for-state wait-interval-seconds'
        'network-load-balancer backend-set delete' = 'backend-set-name force from-json help if-match max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer backend-set get' = 'backend-set-name from-json help if-none-match network-load-balancer-id'
        'network-load-balancer backend-set update' = 'backend-set-name backends force from-json health-checker help if-match is-preserve-source max-wait-seconds network-load-balancer-id policy wait-for-state wait-interval-seconds'
        'network-load-balancer backend-set-health get' = 'backend-set-name from-json help network-load-balancer-id'
        'network-load-balancer backend-set-summary list-backend-sets' = 'all from-json help if-none-match limit network-load-balancer-id page page-size sort-order'
        'network-load-balancer backend-summary list-backends' = 'all backend-set-name from-json help if-none-match limit network-load-balancer-id page page-size sort-order'
        'network-load-balancer health-checker get' = 'backend-set-name from-json help if-none-match network-load-balancer-id'
        'network-load-balancer health-checker update' = 'backend-set-name from-json help if-match interval-in-millis max-wait-seconds network-load-balancer-id port protocol request-data response-body-regex response-data retries return-code timeout-in-millis url-path wait-for-state wait-interval-seconds'
        'network-load-balancer listener create' = 'default-backend-set-name from-json help if-match max-wait-seconds name network-load-balancer-id port protocol wait-for-state wait-interval-seconds'
        'network-load-balancer listener delete' = 'force from-json help if-match listener-name max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer listener get' = 'from-json help if-none-match listener-name network-load-balancer-id'
        'network-load-balancer listener update' = 'default-backend-set-name from-json help if-match listener-name max-wait-seconds network-load-balancer-id port protocol wait-for-state wait-interval-seconds'
        'network-load-balancer listener-protocols list-network-load-balancers-protocols' = 'all from-json help limit page page-size sort-order'
        'network-load-balancer listener-summary list-listeners' = 'all from-json help if-none-match limit network-load-balancer-id page page-size sort-order'
        'network-load-balancer network-load-balancer change-compartment' = 'compartment-id from-json help if-match max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer network-load-balancer create' = 'backend-sets compartment-id defined-tags display-name freeform-tags from-json help is-preserve-source-destination is-private listeners max-wait-seconds network-security-group-ids reserved-ips subnet-id wait-for-state wait-interval-seconds'
        'network-load-balancer network-load-balancer delete' = 'force from-json help if-match max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer network-load-balancer get' = 'from-json help if-none-match network-load-balancer-id'
        'network-load-balancer network-load-balancer list' = 'all compartment-id display-name from-json help lifecycle-state limit page page-size sort-by sort-order'
        'network-load-balancer network-load-balancer update' = 'defined-tags display-name force freeform-tags from-json help if-match is-preserve-source-destination max-wait-seconds network-load-balancer-id wait-for-state wait-interval-seconds'
        'network-load-balancer network-load-balancer update-network-security-groups' = 'force from-json help if-match max-wait-seconds network-load-balancer-id network-security-group-ids wait-for-state wait-interval-seconds'
        'network-load-balancer network-load-balancer-health get' = 'from-json help network-load-balancer-id'
        'network-load-balancer network-load-balancer-health list' = 'all compartment-id from-json help limit page page-size sort-by sort-order'
        'network-load-balancer network-load-balancing-policy list-network-load-balancers-policies' = 'all from-json help limit page page-size sort-order'
        'network-load-balancer work-request get' = 'from-json help work-request-id'
        'network-load-balancer work-request list' = 'all compartment-id from-json help limit page page-size'
        'network-load-balancer work-request-error list' = 'all compartment-id from-json help limit page page-size work-request-id'
        'network-load-balancer work-request-log-entry list-work-request-logs' = 'all compartment-id from-json help limit page page-size work-request-id'
    }
    return $ociCommandsToLongParams
}

function GetOciCommandsToShortParams_network_load_balancer() {
    $ociCommandsToShortParams = @{
        'network-load-balancer backend create' = '? h'
        'network-load-balancer backend delete' = '? h'
        'network-load-balancer backend get' = '? h'
        'network-load-balancer backend update' = '? h'
        'network-load-balancer backend-health get' = '? h'
        'network-load-balancer backend-set create' = '? h'
        'network-load-balancer backend-set delete' = '? h'
        'network-load-balancer backend-set get' = '? h'
        'network-load-balancer backend-set update' = '? h'
        'network-load-balancer backend-set-health get' = '? h'
        'network-load-balancer backend-set-summary list-backend-sets' = '? h'
        'network-load-balancer backend-summary list-backends' = '? h'
        'network-load-balancer health-checker get' = '? h'
        'network-load-balancer health-checker update' = '? h'
        'network-load-balancer listener create' = '? h'
        'network-load-balancer listener delete' = '? h'
        'network-load-balancer listener get' = '? h'
        'network-load-balancer listener update' = '? h'
        'network-load-balancer listener-protocols list-network-load-balancers-protocols' = '? h'
        'network-load-balancer listener-summary list-listeners' = '? h'
        'network-load-balancer network-load-balancer change-compartment' = '? c h'
        'network-load-balancer network-load-balancer create' = '? c h'
        'network-load-balancer network-load-balancer delete' = '? h'
        'network-load-balancer network-load-balancer get' = '? h'
        'network-load-balancer network-load-balancer list' = '? c h'
        'network-load-balancer network-load-balancer update' = '? h'
        'network-load-balancer network-load-balancer update-network-security-groups' = '? h'
        'network-load-balancer network-load-balancer-health get' = '? h'
        'network-load-balancer network-load-balancer-health list' = '? c h'
        'network-load-balancer network-load-balancing-policy list-network-load-balancers-policies' = '? h'
        'network-load-balancer work-request get' = '? h'
        'network-load-balancer work-request list' = '? c h'
        'network-load-balancer work-request-error list' = '? c h'
        'network-load-balancer work-request-log-entry list-work-request-logs' = '? c h'
    }
    return $ociCommandsToShortParams
}