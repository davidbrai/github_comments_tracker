angular.module('threads', ['ngResource']).
        factory('Threads', function($resource, $http)
{
    return {
        all: $resource('/threads/all'),
        mine: $resource('/threads'),
        markAsRead: function(threadId) {
            $http.post('/thread/' + threadId + '/mark_as_read');
        }
    };
});
