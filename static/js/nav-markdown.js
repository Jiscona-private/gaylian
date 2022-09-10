document.write(`
<nav class="navbar sticky-top navbar-expand-lg" style="background-color: #e3f2fd;">
    <div class="container-fluid">
        <a class="navbar-brand" href="http://gaylian.net">
        <img src="../static/img/gaylian_50.png" alt="Logo" width="40" height="40">
        </a>
    <a class="navbar-brand fs-3 nav-shadow" href="http://gaylian.net" style="padding-bottom: 10px;">gaylian.net</a>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
            <a class="nav-link nav-cloud" href="http://gaylian.net/cloud/new">Cloud</a>
        </li>
        <li class="nav-item color-dinger">
            <a class="nav-link nav-cloud small-dinger" href="http://gaylian.net/cloud">Cloud-Suche</a>
        </li>
        <li class="nav-item">
            <a class="nav-link nav-notes" href="http://gaylian.net/notes/new">Notes</a>
        </li>
        <li class="nav-item">
            <a class="nav-link nav-school" href="http://gaylian.net/school/new">School</a>
        </li>
        <li class="nav-item">
            <a class="nav-link nav-school small-dinger" href="http://gaylian.net/school">School-Suche</a>
        </li>
        <li class="nav-item nav-mail">
            <a class="nav-link" href="http://gaylian.net/mail">Mail-Service</a>
        </li>      
        <li class="nav-item nav-coming">
            <i class="nav-link disabled">more coming soon...</i>
        </li>
        </ul>
        <form class="d-flex" role="search" style="margin-block-end: 0em;">
            <input class="form-control me-2" type="text" name="code" id="searchDocWithCode" placeholder="Markdown suchen" aria-label="Search">
            <input type="button" class="btn btn-outline-success" name="search" value="Search" onclick="searchDoc()">
        </form>
    </div>
    </div>
</nav>
`)