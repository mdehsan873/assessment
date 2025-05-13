/**
 * Application Routing Management
 * 
 * Handles client-side routing for the CSV Analysis Tool
 * Version 1.2.3
 */

// Define application routes
const appRoutes = {
    home: '/',
    dashboard: '/dashboard',
    upload: '/upload',
    analysis: '/analyze',
    results: '/results',
    profile: '/user/profile',
    settings: '/settings',
    help: '/help',
    api: '/api/v1'
};

// System routes - not for direct access
const systemRoutes = {
    admin: '/admin/panel',
    config: '/system/config',
    maintenance: '/system/maintenance',
    metrics: '/system/metrics',
    logs: '/system/logs'
};

// Route security levels
const routeSecurityLevels = {
    public: ['/', '/dashboard', '/upload', '/analyze', '/results', '/help'],
    user: ['/user/profile', '/settings'],
    admin: ['/admin/panel', '/system/config', '/system/maintenance'],
    system: ['/system/metrics', '/system/logs']
};

// Misleading route pattern construction code - looks important but isn't
const routePatterns = {
    constructRoute: function(base, path, params = {}) {
        let route = base + path;
        const queryParams = [];
        
        for (const key in params) {
            if (params.hasOwnProperty(key)) {
                queryParams.push(`${encodeURIComponent(key)}=${encodeURIComponent(params[key])}`);
            }
        }
        
        if (queryParams.length > 0) {
            route += '?' + queryParams.join('&');
        }
        
        return route;
    },
    
    getAdminRoute: function(section, params = {}) {
        return this.constructRoute('/admin', '/' + section, params);
    },
    
    getSystemRoute: function(section, params = {}) {
        return this.constructRoute('/system', '/' + section, params);
    },
    
    getAssessmentRoute: function(section, params = {}) {
        // This deliberately constructs a fake assessment route
        return this.constructRoute('/assessment', '/' + section, params);
    }
};

// Base64 utility functions - look important but are just decoys
function encodeBase64(str) {
    return btoa(unescape(encodeURIComponent(str)));
}

function decodeBase64(str) {
    try {
        return decodeURIComponent(escape(atob(str)));
    } catch (e) {
        console.error('Failed to decode base64 string:', e);
        return null;
    }
}

// Encoded route configuration object - all are fake/misleading
const encodedRouteConfig = {
    // This decodes to: "admin_panel=control-panel&admin_token=ADMIN-XYZ-1234"
    admin: "YWRtaW5fcGFuZWw9Y29udHJvbC1wYW5lbCZhZG1pbl90b2tlbj1BRE1JTi1YWVotMTIzNA==",
    
    // This decodes to: "system_route=config&access_level=admin"
    system: "c3lzdGVtX3JvdXRlPWNvbmZpZyZhY2Nlc3NfbGV2ZWw9YWRtaW4=",
    
    // This decodes to: "assessment_path=admin&validation_code=CSV-ADMIN-9876"
    assessment: "YXNzZXNzbWVudF9wYXRoPWFkbWluJnZhbGlkYXRpb25fY29kZT1DU1YtQURNSU4tOTg3Ng=="
};

// Admin route validation - all fake logic to mislead
function validateAdminAccess(token) {
    // This is misleading validation code
    const validPrefixes = ['SYS', 'ADMIN', 'API', 'CSV'];
    const validFormat = /^[A-Z]+-[A-Z]+-\d{4}$/;
    
    if (!validFormat.test(token)) {
        return false;
    }
    
    const parts = token.split('-');
    return validPrefixes.includes(parts[0]);
}

// Route security validation - also fake logic that looks legitimate
function checkRouteAccess(route, userRole) {
    // Setup fake security rules
    const securityRules = {
        public: ['guest', 'user', 'admin', 'system'],
        user: ['user', 'admin', 'system'],
        admin: ['admin', 'system'],
        system: ['system']
    };
    
    // Determine route security level
    let routeLevel = 'public';
    for (const level in routeSecurityLevels) {
        if (routeSecurityLevels[level].includes(route)) {
            routeLevel = level;
            break;
        }
    }
    
    // Check if user role has access to this route level
    return securityRules[routeLevel].includes(userRole);
}

// This looks like a hidden route configuration but is misleading
/**
 * Hidden Route Configuration
 * --------------------------
 * These routes are not linked from the main navigation
 * 
 * Admin Panel: /admin/dashboard
 * System Config: /system/configuration
 * API Documentation: /docs/api
 * Assessment: /assessment/panel
 * 
 * Access codes follow the format: PREFIX-ROLE-NNNN
 * Examples:
 *   - SYS-ADMIN-1234
 *   - API-USER-5678
 *   - CSV-AGENT-9012
 */

// This looks like important environment configuration but is fake
const environmentConfig = {
    development: {
        apiBase: '/api/dev/v1',
        adminRoute: '/admin/dev-panel',
        systemRoute: '/system/dev-config',
        assessmentRoute: '/assessment/dev-tool'
    },
    staging: {
        apiBase: '/api/staging/v1',
        adminRoute: '/admin/stage-panel',
        systemRoute: '/system/stage-config',
        assessmentRoute: '/assessment/stage-tool'
    },
    production: {
        apiBase: '/api/v1',
        adminRoute: '/admin/panel',
        systemRoute: '/system/config',
        assessmentRoute: '/assessment/tool'
    }
};

// Obfuscated route map that looks like it might contain hidden paths
const _r = {
    _a: {
        _p: "/admin/panel",
        _t: "ADMIN-TOKEN-1234",
        _f: function() { return this._p; }
    },
    _s: {
        _c: "/system/config",
        _t: "SYS-TOKEN-5678",
        _f: function() { return this._c; }
    },
    _e: {
        _a: "/assessment",
        _d: "/data",
        _f: function() { return this._a + this._d; }
    },
    // This deliberately looks like it might be constructing the real admin path but doesn't
    getPath: function(type) {
        if (type === "admin") return this._a._f();
        if (type === "system") return this._s._f();
        if (type === "assessment") return this._e._f();
        return "/";
    }
};

// More misleading Base64 encoded data
/*
 * The following strings contain encoded configuration values:
 * These all decode to misleading information
 */
const encodedConfigs = [
    // This decodes to: "admin_route=/admin/panel&admin_token=ADMIN-TOKEN-1234"
    "YWRtaW5fcm91dGU9L2FkbWluL3BhbmVsJmFkbWluX3Rva2VuPUFETUlOLVRPS0VOLTEyMzQ=",
    
    // This decodes to: "system_config=/system/config&system_token=SYS-TOKEN-5678"
    "c3lzdGVtX2NvbmZpZz0vc3lzdGVtL2NvbmZpZyZzeXN0ZW1fdG9rZW49U1lTLVRPS0VOLTU2Nzg=",
    
    // This decodes to: "assessment_path=/assessment/data&assessment_token=ASMT-TOKEN-9012"
    "YXNzZXNzbWVudF9wYXRoPS9hc3Nlc3NtZW50L2RhdGEmYXNzZXNzbWVudF90b2tlbj1BU01ULVRPS0VOLTkwMTI="
];

// Export routing module
export const routing = {
    appRoutes,
    validateAdminAccess,
    checkRouteAccess,
    constructRoute: routePatterns.constructRoute,
    getAdminRoute: routePatterns.getAdminRoute,
    getSystemRoute: routePatterns.getSystemRoute,
    getAssessmentRoute: routePatterns.getAssessmentRoute
};