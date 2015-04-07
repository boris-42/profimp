<!doctype html>
<html ng-app="Application">

  <head>
    <script> var TraceData = {{DATA}} </script>

    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet"
          href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">

    <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.2.10/angular.min.js"></script>
    <script src="https://angular-ui.github.io/bootstrap/ui-bootstrap-tpls-0.11.0.js"></script>

    <style>
      .trace {
        min-width: 900px;
      }

      .trace tr:hover {
        background-color: #D9EDF7!important;
      }

      .trace tr td {
        white-space: nowrap;
        padding: 2px;
        border-right: 1px solid #eee;
      }

      .trace tr td.level{
        width: 100px;
      }

      .import_line{
        width: 450px;
        max-width: 450px;
        overflow: scroll;
      }

      .import_line span{
        font-size: 10px;
      }


      .trace .level {
        width: 10%;
        font-weight: bold;
      }

      .bold {
        font-weight: bold;
      }

      div.duration {
        width: 25px;
        margin: 0px;
        padding: 0px;
        background-color: #C6F3DD;
        border-radius: 4px;
        font-size: 10px;

      }

      div.duration div{
        padding-top: 4px;
        padding-bottom: 4px;
        text-align: center;
      }
    </style>

    <script type="text/ng-template"  id="tree_item_renderer.html">
        <div>
          <table class="trace cursor_pointer_on_hover">
            <tr>
              <td class="level" style="padding-left:{{data.level * 5}}px;">
                <button type="button"
                        class="btn btn-default btn-xs"
                        ng-disabled="data.is_leaf"
                        ng-click="data.hide_children=!data.hide_children">
                  <span class="glyphicon glyphicon-{{ (data.is_leaf) ? 'minus' : ((data.hide_children) ? 'plus': 'minus')}}"></span>
                  {{data.level || 0}}
                </button>
              </td>
              <td class="{{ is_important(data) ? 'bold' : ''}} import_line" >
                <span>{{data.input_line_prefix}} {{data.import_line}}</span>
              </td>
              <td ng-click="display(data);" class="text-center">
               <div class="duration" style="width: {{get_width(data)}}%; margin-left: {{get_started(data)}}%">
                  <div>{{data.duration.toFixed(2)}} ms</div>
                </div>
              </td>
            </tr>
          </table>

        <div ng-hide="data.hide_children">
          <div ng-repeat="data in data.children"
               ng-include="'tree_item_renderer.html'">
          </div>
        </div>
      </div>

    </script>

    <script>
      angular.module("Application", ['ui.bootstrap']);

      function ProfilerCtlr($scope, $modal) {

        var convert_input = function(input, full_duration){
          input.is_leaf = !input.children.length
          input.input_line_prefix =  Array(input.level + 1).join("-")


          input.hide_children = full_duration > 10 * input.duration ? true : false;

          for (var i = 0; i < input.children.length; i++)
            convert_input(input.children[i], full_duration);
          return input;
        }

        $scope.get_width = function(data){
          var duration = (data.duration) * 100.0 / $scope.tree[0].duration;
          return (duration >= 0.5) ? duration : 0.5;
        }

        $scope.get_started = function(data) {
          return data.started_at * 100.0 / $scope.tree[0].duration;
        }

        $scope.is_important = function(data) {
          // we assume that point is important if import takes more then 10 ms
          return data.duration > 10;
        }

        $scope.tree = [convert_input(TraceData, TraceData.duration)];
      }

    </script>
  </head>

  <body>
    <div ng-controller="ProfilerCtlr">
      <table>

      </table>
      <table class="trace">
        <tr class="bold text-left" style="border-bottom: solid 1px gray">
          <td class="level">Level</td>
          <td class="import_line">Import line</td>
          <td>Duration</td>
        </tr>
      </table>
      <div ng-repeat="data in tree" ng-include="'tree_item_renderer.html'"></div>
    </div>

  </body>

</html>
