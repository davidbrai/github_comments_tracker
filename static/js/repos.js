angular.module('repos', ['ngResource']).
        factory('Repos', function($resource, $http)
{
    return {
        all: $resource('/repos')
    };
});
