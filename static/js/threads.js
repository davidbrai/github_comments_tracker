angular.module('threads', ['ngResource']).
        factory('Threads', function($resource, $http)
{
    return {
        all: $resource('/threads/all'),
        mine: $resource('/threads'),
        markAsRead: function(thread) {
            $http.post('/thread/' + thread.id + '/mark_as_read').success(function() {
                thread.read = true;
            });
        }
    };
});
