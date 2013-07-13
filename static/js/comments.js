
var app = angular.module('comments', ['threads', 'repos']).config(function($routeProvider) {
    $routeProvider.when('/:mode/:repoid', {
        controller:ThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    });

    $routeProvider.when('/:mode/', {
        controller:ThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/mine/'
    });
});

angular.module('comments').filter('fromNow', function() {
    return function(dateString) {
        return moment(new Date(dateString)).fromNow()
    };
});

marked.setOptions({
    gfm: true,
    tables: true,
    breaks: false,
    pedantic: false,
    sanitize: true,
    smartLists: true,
    smartypants: false,
    langPrefix: 'language-',
    highlight:function (code, lang) {
        if (lang == 'js') {
            lang = 'javascript';
        }
        if (lang != undefined && lang in hljs.LANGUAGES) {
            return hljs.highlight(lang, code).value;
        }

        return hljs.highlightAuto(code).value;
    }
});

angular.module('comments').filter('markdown', function() {
    return function(markdownString) {
        return marked(markdownString);
    }
});

angular.module('comments').filter('escapeHtml', function() {
    return function(text) {
        if (text) {
            return text.
                replace(/&/g, '&amp;').
                replace(/</g, '&lt;').
                replace(/>/g, '&gt;');
        }
        return '';
    }
});

function ThreadsCtrl($scope, $routeParams, Threads, Repos) {
    $scope.mode = $routeParams.mode;
    $scope.active_repo_id = $routeParams.repoid;
    $scope.repos = Repos.all.query();
    $scope.threads = Threads.fetch.query({mode: $scope.mode, active_repo_id: $scope.active_repo_id});

    if ($scope.mode == 'mine') {
        $scope.unreadFilter = {read: 'false'};
        $scope.markAsRead = Threads.markAsRead;
    }
}