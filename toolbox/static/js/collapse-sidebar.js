$(document).ready(function () {

    $('#collapse-btn').click(collapseSidebar);

    function collapseSidebar() {
        $('#sidebar').toggleClass('sidebar-collapsed');
        $('#collapse-btn i').toggleClass('fa-caret-left fa-caret-right');
    }

});