document.write(`
        <div aria-live="polite" aria-atomic="true" class="position-relative">
            <div class="toast-container top-0 end-0 p-3">
                {% if error %}
                <div class="toast show toast-anzeige-1 bottom-0 end-0" role="alert" aria-live="assertive" aria-atomic="true">
                    <div class="toast-header">
                        <img src="../static/img/gaylian_50_yellow.png" class="rounded me-2" alt="gaylian: Error" style="width: 13%;">
                        <strong class="me-auto">Datei Löschen</strong>
                        <small class="text-muted">Schließen</small>
                        <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                    </div>
                        <div class="toast-body">
                            Sind Sie sicher, dass die Datei
                            <a style="color: red;">{{ name }}</a>
                            endgültig gelöscht werden soll?
                            <div class="mt-2 pt-2 border-top ">
                                <form method="post">
                                    <button type="button" class="btn btn-outline-danger toast-button-1">Datei löschen!</button>
                                </form>
                            </div>
                        </div>
                </div>
                {% endif %}
            </div>
        </div>
`)