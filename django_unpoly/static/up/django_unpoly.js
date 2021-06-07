// Unpoly Configuration:
up.radio.config.hungry.push("#djDebug");

// Initialize Django Debug Toolbar for Unpoly requests
up.compiler('#djDebug', function(element){
    djdt.init();
});
