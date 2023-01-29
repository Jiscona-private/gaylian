//user management element
headElement = ""

if (document.cookie) {
  username = document.cookie.split(";")[1].split("=")[1]
  headElement=`
  <li class="nav-item dropdown">
    <div class="dropdown">
      <a class="nav-coming btn btn_nav dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
        Hi ${username}
      </a>
      <ul class="dropdown-menu dropdown-menu-sm-end">
        <li><a class="dropdown-item" href="/user/files">Meine Dateien</a></li>
        <li><hr class="dropdown-divider"></li>
        <li><a class="dropdown-item" href="/user/logout?username=${username}" data-bs-target="logout">Logout</a></li>
      </ul>
    </div>
  </li>`
} 

else {
  headElement =`
  <li class="nav-item" style="padding-right: 5px;">
    <a class="nav-coming btn btn_nav" href="/user/login">Login</a>
  </li>`
}

document.write(`
<div class="nav_all">
        <nav class="navbar navbar-expand-lg navbar-scroll">
          <div class="container-fluid">
              <a class="navbar-brand" href="/">
                <img src="../static/img/gaylian_50.png" alt="Logo" width="40" height="40">
              </a>
              <a class="navbar-brand fs-3 nav-shadow" href="/" style="padding-bottom: 10px;">gaylian.net</a>
              <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
              </button>
              <div class="collapse navbar-collapse" id="navbarSupportedContent">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                  <li class="nav-item">
                    <a class="nav-cloud btn btn_nav" href="/cloud/new">Cloud</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-cloud btn btn_nav2" href="/cloud">Cloud-Suche</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-notes btn btn_nav" href="/notes/new">Notes</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-school btn btn_nav" href="/school/new">School</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-school btn btn_nav2" href="/school">School-Suche</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-mail btn btn_nav" href="/mail">gtc</a>
                  </li>
                </ul>
                <ul class="navbar-nav">
                  ${headElement}
                </ul>
                <div style="padding-bottom: 1px;">
                  <button class="navbar-toggler_index navbar-text" type="button" data-bs-toggle="collapse" data-bs-target="#navbarToggleExternalContent" aria-controls="navbarToggleExternalContent" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                  </button>
                </div>
              </div>
          </div>
        </nav>
        <div class="collapse collapse_content" id="navbarToggleExternalContent">
          <div class="container text-center div_nav_cola">
            <div class="row align-items-center">
              <div class="p-3">
                <h5 class="h4">gaylian.net | Weitere Links</h5>
                <span class="text-muted">Ihre erweiterte Navigation</span>
              </div>
              <div class="p-2">
                <form class="d-flex" role="search" method="post" action="/cloud/search">
                  <input class="form-control me-2" type="text" name="code" id="searchDocWithCode" placeholder="Datei suchen" aria-label="Search">
                  <input type="button" class="btn btn-outline-success" name="search" value="Search" onclick="searchDoc()">
                </form>
              </div>
              <div class="p-2">
                  <form class="d-flex" role="search">
                    <input class="form-control me-2" type="text" name="code" id="searchDocWithCode" placeholder="Markdown suchen" aria-label="Search">
                    <input type="button" class="btn btn-outline-success" name="search" value="Search" onclick="searchDoc()">
                </form>
              </div>
            </div>
          </div>
          <div class="container text-center div_nav_cola">
            <div class="row align-items-center">
              <div class="col"></div>
              <div class="col">
                <form class="d-flex">
                  <input type="button" class="form-control btn btn-outline-dark" onclick="edit()" value="Diese Datei bearbeiten">
                </form>
              </div>
              <div class="col"></div>
            </div>
          </div>
          <hr>
          <div class="nav-mobile-footer">
            <ul class="nav justify-content-center text-center">
              <li class="nav-item footer-middle">
                <a class="btn btn_footer" href="/agb">AGB</a>
              </li>
              <li class="nav-item footer-middle">
                <a class="btn btn_footer" href="/cookies">Cookies</a>
              </li>
              <li class="nav-item">
                <a class="nav-link disabled">© 2023 by Bonarium Holdings. Alle Rechte sind reserviert.<br>
                  gaylian.net ist ein Service von Bonarium Holdings.</a>
              </li>
              <li class="nav-item footer-middle">
                <a class="btn btn_footer" href="/mission">Auftrag</a>
              </li>
              <li class="nav-item footer-middle">
                <a class="btn btn_footer" href="/impressum">Impressum</a>
              </li>
            </ul>
            <div class="container text-center">
              <div class="row align-items-center">
                <hr style="margin-top: 10px;">
                <div class="p-2">
                  basiert. basierter. gaylian.
                </div>
                <div class="col" style="padding-bottom: 10px;">
                  ALPHA-Version (0.1) <span style='font-size: 20px;'>&#128074;</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
`)