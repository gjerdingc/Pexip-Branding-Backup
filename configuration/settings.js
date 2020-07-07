var applicationSettings = {
    serverAddress: (window.srv || window.nw) ? null : window.location.host, // Can be overridden with a host name or ip

    defaultDialOutProtocol: 'sip', // sip | h323 | mssip | rtmp | auto

    languages: {
        'Dansk (Danish)': 'configuration/languages/da-dk.json',
        'English (US)': 'configuration/languages/en-us.json',
	'Svenska (Swedish)': 'configuration/languages/sv-se.json',
        'Norsk Bokmål (Norwegian)': 'configuration/languages/no-nb.json'
    },

    bandwidths: [{
        name: 'IDS_BANDWIDTH_LOW', 
        value: 256
    }, {
        name: 'IDS_BANDWIDTH_MEDIUM', 
        value: 576
    }, {
        name: 'IDS_BANDWIDTH_HIGH', 
        value: 1264
    }, {
        name: 'IDS_BANDWIDTH_MAXIMUM', 
        value: 1864
    }],

    defaultDialOutRole: 'host', // 'host' or 'guest'

    enableFullMotionPresentation: true,

    // Uncomment the following line to hide registration settings from the desktop client UI
    // desktopClientHideRegistrationSettings: true,

    // Uncomment the following line to hide connection settings from the desktop client UI
    // desktopClientHideConnectionSettings: true,

    // Uncomment the next line and specify an img path to override conference-avatar:
    overrideConferenceAvatar: 'configuration/themes/default/conference-avatar.jpg',

    // Uncomment one of the next lines to specify a client-side TURN server to use
    // turnServer: { url: 'turn:turn.example.com', username: 'user', credential: 'pass' },
    // turnServer: { url: 'turn:turn.example.com:443?transport=tcp', username: 'user', credential: 'pass' },

    // Uncomment and reconfigure the next line if you use a customized screensharing extension
    // screenshareApi: 'pexGetScreen',

    // controlGatewayCalls: true, // Uncomment this line to show the conference-control menu in GW calls
};

// Default configuration to apply to first-time users
var defaultUserSettings = {
    language: 'configuration/languages/no-nb.json',

    defaultBandwidth: 576, // Make sure the value is in applicationSettings.bandwiths
	screenshareFrameRate: 5,						

    promptDisconnect: true,
    promptMedia: true,
    analyticsReportingEnabled: true,
    fullMotionPresentationByDefault: false,
    muteOnJoin: false,
    startMinimized: false,
    sideBarHidden: false,
    sideBarHiddenInGW: true,
};
