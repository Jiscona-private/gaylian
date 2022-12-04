error = document.getElementById("error").value

if (error) {
  document.write(`
    <div aria-live="polite" aria-atomic="true" class="position-relative">
        <div class="toast-container top-0 end-0 p-3" style="padding-top: 15px;">
            <div class="toast show toast-anzeige-2 bottom-0 end-0" role="alert" aria-live="assertive" aria-atomic="true">
              <div class="toast-header">
                <img src="../static/img/gaylian_50_red.png" id="toastLogo" class="rounded me-2" alt="gaylian: Error" style="width: 13%;">
                <strong class="me-auto">gaylian-Fehlermeldung</strong>
                <small class="text-muted">Schließen</small>
                <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
              </div>
              <div class="toast-body">
                Das hat nicht funktioniert :( <br> Der Fehler lautet:
                <a style="color: red;">${error}</a>  
              </div>
            </div>
        </div>
    </div>    
  `)
}
