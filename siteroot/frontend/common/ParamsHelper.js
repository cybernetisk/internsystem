/**
 * This factory assists in updating params in the url
 * and running a function when it changes
 */
angular.module('cyb.oko').factory('ParamsHelper', function ($location, $stateParams) {
    return {
        track: function (scope, variables, watchers, callback) {
            if (arguments.length == 3) {
                callback = watchers;
                watchers = {};
            }

            var q = {};
            var obj = {
                run: function () {
                    q = {};
                    variables.forEach(function (name) {
                        q[name] = $stateParams[name] || null;
                    });

                    callback(q);
                },
                update: function (param, value) {
                    if (param in q && q[param] == value) {
                        console.log("discard no real change to", param);
                        return;
                    }
                    console.log("update", param, "to", value);
                    $location.search(param, value);
                    $stateParams[param] = value;
                    this.run(); // TODO: only run once at end of "updates"?
                }
            };

            scope.$watch(function () { return $location.search(); }, function (newP, oldP) {
                console.log("search changed");
                variables.forEach(function (name) {
                    var x1 = oldP[name] || null;
                    var x2 = newP[name] || null;
                    if (x1 !== x2) {
                        console.log("updating", name, "from", oldP[name], "to", newP[name]);
                        obj.update(name, newP[name]);
                    }
                });
            });

            angular.forEach(watchers, function (dest, source) {
                scope.$watch(source, function (val) {
                    if (typeof val != 'undefined') {
                        // TODO: sette default properties som ikke legges i $location.search() ?
                        if (dest == 'page' && val == 1) val = null;
                        console.log("watched change in", source, "so updating", dest, "to", val);
                        obj.update(dest, val);
                    }
                });
            });

            return obj;
        }
    };
});
