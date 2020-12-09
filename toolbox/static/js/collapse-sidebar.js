$(document).ready(function () {

    $('#collapse-btn').click(collapseSidebar);

    function collapseSidebar() {
        $('#sidebar').toggleClass('sidebar-collapsed');
    }

});