$(document).ready(function () {

  navlink = $("a.nav-link");

  // Move the nav item highlight
  function moveHighlight() {
    /**var activeNavItem = $("li.nav-item.active")
        highlight = $("img.active-highlighter");
        highlight.addClass("yay");*/
  }

  navlink.on("click", moveHighlight);

});