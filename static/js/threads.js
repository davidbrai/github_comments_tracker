angular.module('threads', ['ngResource']).
        factory('Threads', function($resource, $http)
{
    return {
        fetch: $resource('/threads/:mode/:active_repo_id',{mode:'@mode', active_repo_id:'@active_repo_id'}),
        markAsRead: function(thread) {
            $http.post('/thread/' + thread.id + '/mark_as_read').success(function() {
                thread.read = true;
            });
        }
    };
});
