angular.module('threads', ['ngResource']).
        factory('Thread', function($resource)
{
    var Thread = $resource('/threads', {}, {});

    return Thread;
});
