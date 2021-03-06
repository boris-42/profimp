<!doctype html>
<html ng-app="Application">
  <head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Imports profiling results</title>
  <style>
    body { margin:0 0 50px; padding:0; font-size:14px; font-family:Helvetica,Arial,sans-serif }
    table { border-collapse:collapse; border-spacing:0; width:100% }
    thead th { text-align:left; padding:8px 4px; color:#000; border:2px solid #ddd; border-width:0 0 2px 0 }
    tbody tr:hover { background:#d9edf7; cursor:pointer }
    tbody td { text-align:left; solid #ddd; padding:3px 2px; color:#333; font-size:12px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; white-space: nowrap; font-family:monospace }
    .header { text-align:left; background:#333; font-size:18px; padding:13px 0; margin-bottom:20px; color:#fff; background-image:linear-gradient(to bottom, #444 0px, #222 100%) }
    .header a, .header a:visited, .header a:focus { color:#999; text-decoration: none }
    .leaf { width:17px; border:none; padding:0; background:none; border:none; text-align:center; }
    tbody td span { color: gray; }
    td.import_line { max-width: 400px; overflow: hidden; padding-right: 20px}
    td.duration { width:40%; padding:2px 0; overflow: visible; color: gray; }
    td.duration div { text-align:center; padding:3px 0; line-height:12px; background:#c6f3dd; border-radius:2px; overflow: visible; white-space: nowrap; }
    .content-wrap {margin:0 auto; padding:0 5px}
    @media only screen and (min-width: 320px)  { .content-wrap { width:900px  } .content-main { width:600px } }
    @media only screen and (min-width: 900px)  { .content-wrap { width:880px  } .content-main { width:590px } }
    @media only screen and (min-width: 1000px) { .content-wrap { width:980px  } .content-main { width:690px } }
    @media only screen and (min-width: 1100px) { .content-wrap { width:1080px } .content-main { width:790px } }
    @media only screen and (min-width: 1200px) { .content-wrap { width:1180px } .content-main { width:890px } }
  </style>

  <script>var TraceData = {{DATA}}</script>
  <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.10/angular.min.js"></script>
  <script>
    angular.module("Application", []);

    function ProfilerCtlr($scope) {
      var idx = 0;
      $scope.max_duration = TraceData["duration"];
      $scope.tree = {0: {parent: 0, is_expandable: true, is_expanded: true}};
      $scope.imports = [];
      var append_imp = function(imp, parent_idx, level){
        idx++;
        var this_idx = idx;
        $scope.imports.push({level: level,
                      index: idx,
                      module: imp.module,
                      file: imp.filepath,
                      import_line: imp.import_line,
                      duration: imp.duration,
                      started_at: imp.started_at})

        $scope.tree[idx] = {parent: parent_idx,
                            is_expandable: imp.children.length,
                            is_expanded: (level < 4) && imp.duration > $scope.max_duration / 20}
        for (var i in imp.children) {
          append_imp(imp.children[i], this_idx, level + 1)
        }
      }
      append_imp(TraceData, 0, 0);
      $scope.duration_bar_style = function(imp){
        var margin_left = Math.ceil((imp.started_at / $scope.max_duration) * 100);

        /* Do not overflow right table border
         * FIXME: This must be done better
        */
        if (margin_left > 75) {
          margin_left = 75
        }
        return {'margin-left': margin_left + "%",
                width: Math.round((imp.duration / $scope.max_duration) * 100) + "%"};
      }

      var has_collapsed_parent = function(idx) {
        if (idx == 0) { return false }
        var parent_idx = $scope.tree[idx].parent;

        if (!$scope.tree[parent_idx].is_expanded) {
          return true
        }
        return has_collapsed_parent(parent_idx)
      }

      $scope.is_hidden = function(imp) {
        return has_collapsed_parent(imp.index)
      }

      $scope.toggle_expand = function(imp) {
        if ($scope.tree[imp.index].is_expandable) {
          $scope.tree[imp.index].is_expanded = !$scope.tree[imp.index].is_expanded
        }
      }

      var repeat_str = function(str, repeat){
          var s = "";
          for (var i=0; i<repeat; i++) { s += str };
          return s
      }
      $scope.indent = function(str, num) {
        if (num) {
          return repeat_str(str, (str, num * 2) - 3)
        }
        return ''
      }
    }
  </script>
</head>

<body ng-controller="ProfilerCtlr">
  <div class="header">
    <div class="content-wrap">
      <a href="https://github.com/boris-42/profimp">ProfImp</a>&nbsp;
      <span>imports profiling results</span>
    </div>
  </div>

  <div class="content-wrap">
    <table>

    </table>
    <table class="trace">
      <thead>
        <tr>
          <th>Import line</th>
          <th>Duration</th>
        </tr>
      </thead>
      <tbody>
        <tr ng-hide="is_hidden(imp)" ng-click="toggle_expand(imp)"
            ng-repeat="imp in imports track by $index"
            title="{{imp.module}} ({{imp.file}})">
          <td class="import_line">
            <span>{{indent('&nbsp;', imp.level)}}</span>
            <span ng-show="imp.level">&#9584;</span><span class="leaf" ng-hide="tree[imp.index].is_expandable">&#9472;&#9472;&nbsp;{{imp.level}}</span>
            <span ng-show="tree[imp.index].is_expandable"
                  n-g-click="tree[imp.index].is_expanded = !tree[imp.index].is_expanded">
              <span ng-hide="tree[imp.index].is_expanded">&#9654;&nbsp;{{imp.level}}</span>
              <span ng-show="tree[imp.index].is_expanded">&#9661;&nbsp;{{imp.level}}</span>
            </span>
            <span ng-show="imp.level">&#9472;&#9472;&#9472;&#9472;</span>
            {{imp.input_line_prefix}} {{imp.import_line}}
          </td>
          <td class="duration">
            <div ng-style="duration_bar_style(imp)">{{imp.duration.toFixed(2)}} ms</div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>

</body>
</html>
