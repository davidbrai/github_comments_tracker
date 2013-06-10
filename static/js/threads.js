angular.module('threads', ['ngResource']).
        factory('Threads', function($resource)
{
    return {
        all: $resource('/threads/all'),
        mine: $resource('/threads')
    };
});
