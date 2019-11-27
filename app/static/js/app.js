$(function () {
	$('body').on('click','a.view-tables', function (evt) {
		$('a.view-tables').removeClass('active');
		$(this).addClass('active');
    	evt.preventDefault();
		db = $(this).data('db');
		$('div#table_detail div.card-header').html('Выберите таблицу');
		$('div#table_detail div.card-body').html('');
		$('div#table_list div.card-header').html('Загрузка...');
		$('div#table_list div.card-body').html('<div class="cssload-thecube"><div class="cssload-cube cssload-c1"></div><div class="cssload-cube cssload-c2"></div>	<div class="cssload-cube cssload-c4"></div>	<div class="cssload-cube cssload-c3"></div></div>');
        $.ajax({
        	type: "GET",
			contentType: "application/json; charset=utf-8",
            url: "/api/"+db+'/tables',
            success: function (msg) {
				html = build_table_list(msg);
				$('div#table_list div.card-header').html(msg.database);
				$('div#table_list div.card-body').html(html);
            },
            error: function (xhr, status, error) {
				$('div#table_list div.card-body').html("Ошибка данных");
       		}
   		})
	})

	$('body').on('click','a.table-detail', function (evt) {
    	evt.preventDefault();
		db = $(this).data('db');
		table = $(this).data('table');
		node = $(this).data('node');
		$('div#table_detail div.card-header').html('Загрузка...');
		$('div#table_detail div.card-body').html('<div class="cssload-thecube"><div class="cssload-cube cssload-c1"></div><div class="cssload-cube cssload-c2"></div>	<div class="cssload-cube cssload-c4"></div>	<div class="cssload-cube cssload-c3"></div></div>');
        $.ajax({
        	type: "GET",
			contentType: "application/json; charset=utf-8",
            url: "/api/"+db+'/'+table+'/detail?node='+node,
            success: function (msg) {
				$('div#table_detail div.card-header').html(msg.database+'.'+msg.table+' ['+msg.node+']');
				html = build_table_detail(msg);
				$('div#table_detail div.card-body').html(html);
            },
            error: function (xhr, status, error) {
				$('div#table_detail div.card-body').html('Ошибка данных');
       		}
   		})
	})
});




function build_table_detail(msg) {
	var table=msg.table;
	var db=msg.database;
	var node=msg.node;
	var create_table_query=msg.create_table_query;
	var html='<pre>';
	html+=sqlFormatter.format(create_table_query);
	html+='</pre>';
	return html;
}



function check_table_names(node, nodes) {
    if(node in nodes) return true;
    return false;
}


function check_table_create_query(nodes) {
	var tmp = undefined;
	for (var node in nodes) {
		str = nodes[node].create_table_query;
		if (tmp === undefined) {
			tmp = str;
		} else {
			if (tmp !== str ) {
				return false;
			}
		}
	}
	return true;
}

function build_table_list(msg) {
	var nodes = msg.nodes;
	var tables = msg.tables;
	var db = msg.database;
	var html='<div style="text-align:left;" id="'+db+'_accordion">';
	html+='<table class="table table-hover" style="margin:0;">';
	for(var table in tables) {
		nodes_html='<table class="table table-sm" style="margin:0;">';
		table_struct_is_valid = check_table_create_query(tables[table].nodes);
		table_in_all_nodes=true;
		for (var node in nodes) {
			nodes_html+='<tr class="table-light"><td style="padding-left:30px;"><span>'+nodes[node]+'</span>';
			if (!check_table_names(nodes[node],tables[table].nodes)) {
				nodes_html+='<i data-toggle="tooltip" title="Таблица не найдена" class="fa fa-exclamation-triangle" style="padding:0 5px;float:right;margin-top: 4px;"></i>'
				table_in_all_nodes=false;
			} else {
				nodes_html+='<div style="float:right;font-size: 0.9rem;text-decoration-skip-ink: none;"><a class="table-detail" href="#'+db+'_'+table+'_detail" data-db="'+db+'" data-table="'+table+'" data-node="'+nodes[node]+'">Подробнее</a></div>';
			}
			nodes_html+='</td></tr>';
		}
		nodes_html+='</table>';
		if (table_in_all_nodes && table_struct_is_valid) {
			html+='<tr class="table-success">';
		} else {
			html+='<tr class="table-warning">';
		}
		html+='<td style="padding:0;"><div style="width:100%;padding:0.5rem;"  data-toggle="collapse" data-target="#'+db+'_'+table+'" aria-expanded="false" aria-controls='+db+'"_collapse">';
		html+='<span>'+table+'</span>';
		if (!table_struct_is_valid) {
			html+='<i class="fa fa-exclamation-circle" style="font-size:1.5rem;padding:0 5px;float:right;" title="Разный CREATE TABLE на нодах"></i>';
		}
		if (!table_in_all_nodes) {
			html+='<i class="fa fa-exclamation-circle" style="font-size:1.5rem;padding:0 5px;float:right;" title="Таблица не найдена на одной или нескольких нодах"></i>';
		}
		html+='</div>';
	    html+='<div class="collapse" data-parent="#'+db+'_accordion" id="'+db+'_'+table+'" style="padding:0">';
		html+=nodes_html;
		html+='</div>';
		html+='</td></tr>';
	}
	html+='</table>';
	html+='</div>';
	return html;
}



