
SortTable.className = 'sortable';  // Die Bezeichnung der Klasse der Tabellen, die sortiert werden sollen

// Die Indikatorelemente, die je nach Zustand im Tabellenheader angezeigt werden (hoch, runter, nichts)
SortTable.up 		= String.fromCharCode(9660);
SortTable.alt_up 	= 'Aufwärts sortieren';
SortTable.down 		= String.fromCharCode(9650);
SortTable.alt_down 	= 'Abwärts sortieren';
SortTable.no 		= String.fromCharCode(9664);
SortTable.alt_no 	= 'unsortiert';

SortTable.pointer_color = 'rgb(39, 131, 119)';	// Farbe des Indikatorelement

SortTable.init = function(){
	var ret = [];
	var regEx  = new RegExp('\\b' + SortTable.className + '\\b', 'i');
	var t = document.getElementsByTagName('table');
	for(var i = 0; i < t.length; i++) {
		if(t[i].className && regEx.test(t[i].className)) ret.push(new SortTable(t[i]));
	}
	return ret;
}

// Class
function SortTable(theTable) {
	// lokale Variabeln
	var self = this;
	var r_no_sort = /\bno_sort\b/i; // Spalte nicht sortieren
	var r_force_String = /\bsort_string\b/i; // Zellen immer als String behandeln
	var r_locale_de = /\blocale_de\b/i; // Zahl in der Zelle mit Komma statt Punkt.
	const DATE_DE = /(\d{1,2})\.(\d{1,2})\.(\d{2,4})|(\d{1,2})\.(\d{1,2})\.(\d{2,4})\s*(\d{1,2}):(\d{1,2})/;
    const IP_MATCH= /(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})/;
    
	var tableBody = theTable.tBodies[0];
	var header = theTable.tHead;

	// SortTable Eventhandler - dummy Funktionen
	self.onstart = self.onsort = self.onprogress = function() {};
	
	self.length = function() { return tableBody.rows.length;};
	self.sort = function(spalte) {
		if(spalte < 0) {
			spalte = header.rows[0].cells.length - 1;
		}
		header.rows[0].cells[spalte].onclick();
	};
	
	if(!header) {
		/**
		 exisitert kein Headerelement:
		 neues Headerelement erzeugen und die erste Zeile dorthin umhängen 
		 Header in die Tabelle einfügen
		*/
		header = theTable.createTHead();
		header.appendChild(tableBody.rows[0]); 
		// Wenn die Tabelle ein tFoot Objekt hat, ist der Body [1]
		tableBody = theTable.tBodies[1] || theTable.tBodies[0];
	}
	/**
	Die Headerzeile mit den Events und dem Marker versehen
	**/
	var th = header.rows[0].cells;
	var last_sort;
	var offset = 0; // für colspan
	for(var i = 0; i < th.length; i++) {
		// soll die Spalte sortiert werden
		if(r_no_sort.test(th[i].className)) continue;
		// click Event
		th[i].onclick = ( function() { 
			// Lokale Werte
			var spalte = i + offset;
			var desc = 1;
			var ignoreCase = ((th[i].getAttribute('ignore_case') || th[i].title) == 'ignore_case');
			var forceString = !!r_force_String.test(th[i].className);
			var locale_de = !!r_locale_de.test(th[i].className);
			var pointer = document.createElement('span');
			// Den Zeiger einfügen
			pointer.style.fontFamily = 'Arial';
			pointer.style.fontSize = '80%';
			pointer.style.visibility = 'hidden';
			pointer.innerHTML = SortTable.up;
			pointer.title = SortTable.alt_up;
			th[i].appendChild(pointer);
			// und die Eventfunktion
			return function() {
				self.onstart(new Date());
				// Der Aufruf, der eigentlichen Sortierfunktion
				sort(spalte, desc, ignoreCase, forceString, locale_de);
				// Sortierung umkehren
				desc = -desc;
				// Den Zeiger der zuletzt geklickten Spalte entfernen
				if(last_sort != pointer) {
					if(last_sort) last_sort.style.visibility = 'hidden';
					pointer.style.visibility = '';
					last_sort = pointer;
				}
				pointer.style.color = SortTable.pointer_color;
				pointer.innerHTML = desc < 0 ? SortTable.down : SortTable.up;
				this.title = pointer.title = desc < 0 ? SortTable.alt_down : SortTable.alt_up;
				self.onsort(new Date());
				return false;
			};
		})(); // Funktionsaufruf
		
		th[i].style.cursor = 'pointer';
		if(th[i].getAttribute('colspan')){
			offset += th[i].getAttribute('colspan') -1;
		}
	}
	/**
	Die Sortierfunktion sortiert die angegebene Spalte der Tabelle
	**/
	function sort(spalte, desc, ignoreCase, forceString, locale_de) { 
		// Die Reihen der Tabelle zwischenspeichern
		var rows = [];
		var tr = tableBody.rows;
		var tr_length = tableBody.rows.length;

		for(var i = 0; i < tr_length; i++) {
			rows.push({
				elem: tr[i], 
				value: getValue(tr[i].cells[spalte], ignoreCase, forceString, locale_de) 
			});
            
		}
		// sortieren
		rows.sort( function (a, b) {
			return  a.value.localeCompare ?  desc * a.value.localeCompare(b.value) :
			a.value == b.value ? 0 :
			a.value > b.value ? desc : -desc;
		});
		var tCopy = tableBody.cloneNode(false); // neuer tBody o. Inhalt
		for(var i = 0; i < tr_length; i++) {
            tCopy.appendChild(rows[i].elem);
            self.onprogress(i, rows[i].elem);
		}
		tableBody.parentNode.replaceChild(tCopy, tableBody); // alte Tabelle mit der neuen Tabelle ersetzen
		tableBody = tCopy;
	}
	/********************************************
	 * Hilfsfunktionen
     * getValue of a cell
     * try to find out what kind of value
     * 
	 ********************************************/
    
    function getValue(el, ignoreCase, forceString, locale_de) {
		var val = getText(el).trim();
		if(forceString) return ignoreCase ? val.toLowerCase() : val;
        var d;
        // match an IP and convert it to decimal
        d = val.match(IP_MATCH);
		if(d) {
            return d.slice(0, 4).reduce(function (a, o) {return u(+a << 8) + +o;});
		}
        d = val.match(DATE_DE);
		if(d) {
			if(!d[4]) d[4] = 0; 
			if(!d[5]) d[5] = 0; 
		}
        if(locale_de) val = val.replace(/,/, '.');
		return val == parseFloat(val) ? parseFloat(val) : // Zahl
		d ? (new Date(d[3] + '/' + d[2] + '/' + d[1] + ' ' + d[4] + ':' + d[5]).getTime()) :  // deutsches Datum
		!isNaN(Date.parse(val)) ? Date.parse(val) :
		ignoreCase ? val.toLowerCase() : val;
	}
    function u(n) { return n >>> 0; } 
    
	function getText(td) {
		if(td.getAttribute('my_key')) {
			return td.getAttribute('my_key');
		} else if(td.childNodes.length > 0) {
			// Enthält das Element HTML Knoten
			var input = td.getElementsByTagName('input')[0];
			if(input && input.type == 'text') {
				return input.value;
			} else if(td.getElementsByTagName('select')[0]) {
				return td.getElementsByTagName('select')[0].value;
			} else {
				// Enthält die Zelle HTML Code wird dieser entfernt 
				return td.innerHTML.stripTags();
			}
		} else if(td.firstChild){
				return td.firstChild.data;
		}
		return '';
	}

}

String.prototype.stripTags =  function(){
	return this.replace(/<[^!](?:[^>"']|"[^"]*"|'[^"]*')*>|<!--.*?-->/g,'');
};
String.prototype.trim = function (ws) {
    if(!this.length) return "";
    var tmp = this.ltrim().rtrim();
    return ws ? tmp.replace(/ +/g, ' ') : tmp;
};
String.prototype.rtrim = function () {
    return this.length ? this.replace(/\s+$/g, '') : "";
},
String.prototype.ltrim = function () {
    return this.length ? this.replace(/^\s+/g, '') : '';
};