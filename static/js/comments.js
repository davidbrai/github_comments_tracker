
var app = angular.module('comments', ['threads']).config(function($routeProvider) {
    $routeProvider.when('/', {
        controller:MyThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).when('/all', {
        controller:AllThreadsCtrl, templateUrl:'/static/js/templates/comments-view.html'
    }).otherwise({
        redirectTo:'/'
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

function AllThreadsCtrl($scope, Threads) {
    $scope.mode = 'all';
    $scope.threads = Threads.all.query();
}

function MyThreadsCtrl($scope, Threads) {
    $scope.mode = 'mine';
    $scope.threads = Threads.mine.query();
    $scope.unreadFilter = {read: 'false'};
    $scope.markAsRead = Threads.markAsRead;
}