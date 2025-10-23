from django.urls import path
from Aplicaciones.Salary import views

urlpatterns = [

    path('login/', views.LogIn, name="login_salary"),

    path('', views.Salary, name="inicio_salary"),



    path('adicionales/carga-adicional/', views.CargaAdicional, name="salary_carga_adicional"),

    path('adicionales/carga-adicional/llenar-comboxs-adicional/', views.listarLegajosConceptos, name="salary_carga_adicional_legajos_conceptos"),

    path('adicionales/carga-adicional/guarda-adicional/', views.guardaAdicional, name="salary_guarda_adicional"),

    path('adicionales/carga-adicional-masivo/', views.CargaAdicionalMasivo, name="salary_carga_adicional_masivo"),

    path('adicionales/carga-adicional-masivo/llenar-comboxs-adicional-masivo/', views.listarConceptosCentros, name="salary_carga_adicional_masivo_centros_conceptos"),

    path('adicionales/carga-adicional-masivo/listado-tabla/', views.listarLegajosTablaMasiva, name="salary_carga_listado_tabla_masivo"),

    path('adicionales/carga-adicional-masivo/guarda-adicional-masivo/', views.guardaAdicionalMasivo, name="salary_carga_listado_envia_masivo"),

    path('adicionales/listado-adicional/', views.ListadoAdicional, name="salary_listado_adicional"),

    path('adicionales/listado-adicional/carga-datos-inicio/', views.listarConceptosCentrosEstado, name="salary_listado_adicional_datos_inicio"),

    path('adicionales/listado-adicional/centro-legajos/', views.listarLegajos, name="salary_listado_adicional_listar_legajos"),

    path('adicionales/listado-adicional/llenar-tabla-adicional/', views.listarAdicionalesTabla, name="salary_listado_adicional_completa_tabla_adicional"),

    path('adicionales/listado-adicional/actualiza-adicional/', views.ActualizaAdicional, name="salary_actualiza_adicional"),

    path('adicionales/listado-adicional/elimina-adicional/', views.eliminaAdicional, name="salary_elimina_adicional"),

    path('adicionales/listado-adicional/datos-modifica-adicional/', views.datosModificaAdicional, name="salary_datos_modifica_adicional"),



    path('liquidaciones/carga-liquidacion/', views.CargaLiquidacion, name="salary_carga_liquidacion"),

    path('liquidaciones/carga-liquidacion/guarda-liquidacion/', views.guardaLiquidacion, name="salary_guarda_liquidacion"),

    path('liquidaciones/listado-liquidacion/', views.ListadoLiquidacion, name="salary_listado_liquidacion"),

    path('liquidaciones/listado-liquidacion/llenar-tabla-liquidacion/', views.listarLiquidacionesTabla, name="salary_listado_liquidacion_tabla"),

    path('liquidaciones/listado-liquidacion/datos-modifica-liquidacion/', views.datosModificaLiquidacion, name="salary_listado_modifica_liquidacion"),

    path('liquidaciones/listado-liquidacion/cierre-masivo-liquidacion/', views.cierraLiquidacionMasivo, name="salary_listado_cierre_masivo"),

    path('liquidaciones/listado-liquidacion/actualiza-liquidacion/', views.actualizaLiquidacion, name="salary_listado_actualiza_liquidacion"),




    path('pagos/liquidar/', views.PagosLiquidar, name="salary_liquidar"),

    path('pagos/liquidar/listar-conceptos-centros/', views.listarConceptosCentros, name="salary_liquidar_conceptos_centros"),

    path('pagos/liquidar/listar-legajos-centros/', views.listarLegajos, name="salary_liquidar_conceptos_centros"),

    path('pagos/liquidar/listar-tabla-liquidar/', views.listarAdicionalesTabla, name="salary_listado_liquidar_completa_tabla_liquidar"),

    path('pagos/liquidar/aisgna-liquidacion/', views.asignaLiquidaciones, name="salary_listado_asigna_liquidacion"),


    
#listar-items-cantidad-importe/
    path('pagos/anula-liquidacion/', views.AnularLiquidación, name="salary_anula_liquidacion"),

    path('pagos/anula-liquidacion/listar-liquidaciones-anular/', views.listarLiquidacionesId, name="salary_anula_listar_liquidacion"),

    path('pagos/anula-liquidacion/lista-personal-centros/', views.listarCentrosLegajosP, name="salary_anula_lista_personal_centros"),

    path('pagos/anula-liquidacion/lista-data-tabla-liquidaciones/', views.listarDataLiquidacionesTabla, name="salary_anula_lista_data_tabla_liquidaciones"),

    path('pagos/anula-liquidacion/quita-de-liquidacion/', views.quitaDeLiquidaciones, name="salary_anula_quita_de_liquidacion"),





    path('pagos/imprimir/', views.Imprimir, name="salary_imprimir"),

    path('pagos/imprimir/listar-liquidaciones/', views.listarLiquidacionesIdImprimir, name="salary_anula_listar_liquidacion"),

    path('pagos/imprimir/listar-centro-cantidad-importe/', views.listarCentrosCantidadImporte, name="salary_anula_listar_liquidacion"),

    path('pagos/imprimir/listar-items-cantidad-importe/', views.listarItemsCantidadImporte, name="salary_anula_listar_items_liquidacion"),

    path('pagos/imprimir/imprimir-recibo-planilla-memo/', views.imppresiones, name="salary_anula_listar_items_liquidacion"),





    path('permanencia/importar/', views.ImportarPermanencia, name="salary_importar_permanencia"),

    path('adicionales/importar/', views.ImportarAdicionales, name="salary_importar_adicionales"),

    path('adicionales/importar/subir-excel/', views.subirAdicionales, name="salary_importar_subir_adicionales"),





    path('legajos/importar/', views.ImportarLegajos, name="salary_importar_legajos"),

    path('legajos/importar/surbir-json/', views.subirLegajos, name="salary_importar_json"),

    path('legajos/listar-legajos/', views.ListadoLegajos, name="salary_listar_legajos"),

    path('legajos/listar-legajos/llenar-combox-centros/', views.listarCentrosLegajos, name="salary_listar_centros_legajos"),

    path('legajos/listar-legajos/llenar-combox-legajos/', views.listarLegajos, name="salary_listar_legajos_combox"),

    path('legajos/listar-legajos/llenar-tabla-legajos/', views.listarLegajosTabla, name="salary_listar_legajos_tabla"),




    path('conceptos/carga-concepto/', views.CargaConcepto, name="salary_carga_concepto"),

    path('conceptos/pruebas/', views.pruebas, name="salary_pruebas_concepto"),

    path('conceptos/carga-concepto/guarda-concepto/', views.guardaConcepto, name="guarda_concepto"),

    path('conceptos/listar-conceptos/', views.ListadoConceptos, name="salary_listar_conceptos"),

    path('conceptos/listar-conceptos/llenar-combox/', views.listaConceptos, name="lista_conceptos"),

    path('conceptos/listar-conceptos/listado-tabla/', views.listadoConceptos, name="listado_conceptos"),

    path('conceptos/listar-conceptos/actualiza-concepto/', views.actualizaConcepto, name="actualiza_concepto"),


    path('centros/carga-centro/', views.CargaCentro, name="salary_carga_centro"),

    path('centros/listar-centros/', views.ListadoCentros, name="salary_listar_centros"),

    path('centros/listar-centros/llenar-combox/', views.listaCentros, name="lista_centros"),

    path('centros/carga-centro/guarda-centro/', views.guardaCentros, name="guarda_centros"),

    path('centros/listar-centros/completa-tabla/', views.listaTablaCentros, name="salary_listar_tabla_centros"),

    path('centros/listar-centros/elimina-centro/', views.eliminaCentro, name="salary_listar_elimina_centro"),


]