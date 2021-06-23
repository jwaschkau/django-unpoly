// Unpoly Configuration:
up.radio.config.hungrySelectors.push("#djDebug");

// Initialize Django Debug Toolbar for Unpoly requests
up.$compiler('#djDebug', function(element){
    if (typeof djdt !== "undefined") {
        djdt.init()
    }
})
