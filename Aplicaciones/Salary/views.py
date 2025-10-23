from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.db import connections
from django.shortcuts import redirect
from collections import OrderedDict
import pandas as pd
from datetime import datetime
from fpdf import FPDF
import io
import json
import re
#import locale
#import os

# Create your views here.

def admin_redirect(request):
    return redirect('/administracion-django/ex-salary/')

def LogIn (request):
    return render (request, 'Salary/Inicio/login.html')

@login_required
def Salary(request):
    return render (request, 'Salary/Inicio/index.html')

@login_required
def CargaAdicional(request):
    return render (request, 'Salary/Adicionales/cargaAdicional.html')

@login_required
def CargaAdicionalMasivo(request):
    return render (request, 'Salary/Adicionales/cargaAdicionalMasivo.html')

@login_required
def ListadoAdicional(request):
    return render (request, 'Salary/Adicionales/listadoAdicional.html')

@login_required
def CargaLiquidacion(request):
    return render (request, 'Salary/Liquidaciones/agregarLiquidacion.html')

@login_required
def ListadoLiquidacion(request):
    return render (request, 'Salary/Liquidaciones/listadoLiquidaciones.html')

@login_required
def PagosLiquidar(request):
    return render (request, 'Salary/Pagos/liquidar.html')

@login_required
def AnularLiquidación(request):
    return render (request, 'Salary/Pagos/anularLiquidacion.html')

@login_required
def Imprimir(request):
    return render (request, 'Salary/Pagos/imprimir.html')

@login_required
def ImportarPermanencia(request):
    return render (request, 'Salary/Permanencia/importarPermanencia.html')

@login_required
def ImportarAdicionales(request):
    return render (request, 'Salary/Permanencia/importarAdicionales.html')

@login_required
def ImportarLegajos(request):
    return render (request, 'Salary/Legajos/importarLegajos.html')

@login_required
def ListadoLegajos(request):
    return render (request, 'Salary/Legajos/listadoLegajos.html')

@login_required
def CargaConcepto(request):
    return render (request, 'Salary/Conceptos/agregarConcepto.html')

@login_required
def ListadoConceptos(request):
    return render (request, 'Salary/Conceptos/listadoConceptos.html')

@login_required
def CargaCentro(request):
    return render (request, 'Salary/Centros/agregarCentro.html')

@login_required
def ListadoCentros(request):
    return render (request, 'Salary/Centros/listadoCentros.html')

@login_required
def pruebas(request):
    return render (request, 'Salary/Conceptos/pruebas.html')

@csrf_exempt
def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:

            login(request, user)
            data = "Se inicio sesion."
            return JsonResponse({'Message': 'success', 'data': data})
            
        else:
            data = "No se pudo iniciar sesión, verifique los datos."
            return JsonResponse({'Message': 'Error', 'data': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})
    


#################################### INICIO CONCEPTOS ####################################



@login_required
@csrf_exempt
def guardaConcepto(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.C_Inserta')
        if user_has_permission:
            usuario = str(request.user).upper()
            descripcionConcepto = str(request.POST.get('descripcionNuevoConcepto')).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            SET @Descripcion = %s;
                            SET @Usuario = %s;
                            INSERT INTO S_Conceptos (Descripcion, FechaAlta, Usuario, Estado)
                                    VALUES (@Descripcion, NOW(), @Usuario, 'A')

                        """
                    cursor.execute(sql,[descripcionConcepto,usuario])

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        sql2 = """ 
                            SELECT  ID_SC AS ID, Descripcion AS CONCEPTO,DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                                    CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA,
                                    CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA
                            FROM S_Conceptos
                            WHERE Descripcion = %s AND Usuario = %s
                    
                            """
                        cursor.execute(sql2,[descripcionConcepto,usuario])
                        result = cursor.fetchone()
                        listado_datos = []
                        if result:
                            idConcepto = str(result[0])
                            descripcion = str(result[1])
                            fecha = str(result[2])
                            usuario = str(result[3])
                            fechaModifica = str(result[4])
                            userModifica = str(result[5])
                            datos = {'Id': idConcepto, 'Descripcion': descripcion, 'Fecha': fecha, 'Usuario': usuario, 'FechaModifica': fechaModifica, 'UserModifica': userModifica}
                            listado_datos.append(datos)
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Concepto se creó correctamente.', 'Datos': listado_datos})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

def listaConceptos(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                listado_conceptos = [{'IdConcepto': '0', 'Descripcion': 'TODOS'}]
                sql = """
                        SELECT  ID_SC AS ID, Descripcion AS CONCEPTO
                        FROM S_Conceptos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idConcepto = str(row[0])
                        descripcion = str(row[1])
                        datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion}
                        listado_conceptos.append(datos)
                return JsonResponse({'Message': 'Success', 'Datos': listado_conceptos})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def listadoConceptos(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.C_Ingresa')
        if user_has_permission:
            usuario = str(request.user).upper()
            idConcepto = str(request.POST.get('selectorConcepto')) or '0'
            try:
                with connections['FEE'].cursor() as cursor:
                    cursor.execute("""
                        SELECT ID_SC AS ID, Descripcion AS CONCEPTO, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                            CASE WHEN FechaModificacion IS NULL THEN '-' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA, 
                            CASE WHEN UsuarioModificacion IS NULL THEN '-' ELSE UsuarioModificacion END AS USER_MODIFICA, Estado 
                        FROM S_Conceptos 
                        WHERE (%s = 0 OR ID_SC = %s) 
                        ORDER BY Descripcion;
                    """, (idConcepto,idConcepto))
                    consulta = cursor.fetchall()
                    listado = []
                    if consulta:
                        for row in consulta:
                            idConcepto = str(row[0])
                            descripcion = str(row[1])
                            fechaAlta = str(row[2])
                            user = str(row[3])
                            fechaModifica = str(row[4])
                            userModifica = str(row[5])
                            estado = str(row[6])
                            datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion, 'Alta': fechaAlta, 'Usuario':user, 'FechaModifica':fechaModifica, 'UserModifica': userModifica, 'Estado':estado}
                            listado.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': listado})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    
@login_required
@csrf_exempt
def actualizaConcepto(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.C_Modifica')
        if user_has_permission:
            usuario = str(request.user).upper()
            ID_SC = request.POST.get('idConcepto')
            estado = str(request.POST.get('estado'))
            descripcion = str(request.POST.get('descripcion')).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Conceptos SET  Descripcion = %s, FechaModificacion = NOW(), UsuarioModificacion = %s, Estado = %s 
                            WHERE ID_SC = %s 
                        """
                    cursor.execute(sql,(descripcion,usuario,estado,ID_SC))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        sql2 = """ 
                            SELECT  ID_SC AS ID, Descripcion AS CONCEPTO, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                                    CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA, 
                                    CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA 
                            FROM S_Conceptos 
                            WHERE ID_SC = %s;
                    
                            """
                        cursor.execute(sql2,(ID_SC,))
                        result = cursor.fetchone()
                        if result:
                            listado_datos = []
                            idConcepto = str(result[0])
                            descripcion = str(result[1])
                            fecha = str(result[2])
                            usuario = str(result[3])
                            fechaModifica = str(result[4])
                            userModifica = str(result[5])
                            datos = {'Id': idConcepto, 'Descripcion': descripcion, 'Fecha': fecha, 'Usuario': usuario, 'FechaModifica': fechaModifica, 'UserModifica': userModifica}
                            listado_datos.append(datos)
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Concepto se actualizó correctamente.', 'Datos': listado_datos})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

#################################### FINAL CONCEPTOS ####################################





#################################### INICIO CENTROS COSTOS ####################################

@login_required
@csrf_exempt
def guardaCentros(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.CC_Inserta')
        if user_has_permission:
            abrev = str(request.POST.get('abrev')).upper()
            descripcion = str(request.POST.get('descripcion')).upper()
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                           SET @Abrev = %s;
                        SET @Descripcion = %s;
                        SET @Usuario = %s;

                        INSERT INTO S_CentrosCostos (Abrev, Descripcion, FechaAlta, Usuario, Estado)
                        VALUES (@Abrev, @Descripcion, NOW(), @Usuario, 'A')
                        ON DUPLICATE KEY UPDATE
                            Descripcion = VALUES(Descripcion),
                            FechaAlta = NOW(),
                            Usuario = VALUES(Usuario),
                            Estado = 'A';

                        """
                    cursor.execute(sql,[abrev,descripcion,usuario])

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        sql2 = """ 
                            SELECT  
                                ID_SCC AS ID, 
                                Abrev AS ABREV, 
                                Descripcion AS CONCEPTO, 
                                DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, 
                                Usuario AS USUARIO, 
                                CASE 
                                    WHEN FechaModificacion IS NULL THEN '' 
                                    ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') 
                                END AS MODIFICA,
                                CASE 
                                    WHEN UsuarioModificacion IS NULL THEN '' 
                                    ELSE UsuarioModificacion 
                                END AS USER_MODIFICA
                            FROM 
                                S_CentrosCostos
                            WHERE 
                                Abrev = %s
                                AND Descripcion = %s
                                AND Usuario = %s;
                        """

                        cursor.execute(sql2,[abrev,descripcion,usuario])
                        result = cursor.fetchone()
                        listado_datos = []
                        if result:
                            idCentro = str(result[0])
                            abrev = str(result[1])
                            descripcion = str(result[2])
                            fecha = str(result[3])
                            usuario = str(result[4])
                            fechaModifica = str(result[5])
                            userModifica = str(result[6])
                            datos = {'Id': idCentro, 'Descripcion': descripcion, 'Fecha': fecha, 'Usuario': usuario, 'FechaModifica': fechaModifica, 'UserModifica': userModifica}
                            listado_datos.append(datos)
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Centro se creó correctamente.', 'Datos': listado_datos})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

@login_required
@csrf_exempt
def listaCentros(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                listado_conceptos = [{'Id': '0', 'Descripcion': 'TODOS'}]
                sql = """
                        SELECT  ID_SCC AS ID, Abrev AS ABREV, Descripcion AS DESCRIPCION
                        FROM S_CentrosCostos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idCentro = str(row[0])
                        descripcion = str(row[1]) + ' - ' + str(row[2])
                        datos = {'Id': idCentro, 'Descripcion': descripcion}
                        listado_conceptos.append(datos)
                return JsonResponse({'Message': 'Success', 'Datos': listado_conceptos})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt    
def listaTablaCentros(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.CC_Ingresa')
        if user_has_permission:
            centro = str(request.POST.get('Centro')) or '0'
            try:
                with connections['FEE'].cursor() as cursor:
                    cursor.execute("""
                        SELECT Abrev AS ID, Descripcion AS CONCEPTO, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                            CASE WHEN FechaModificacion IS NULL THEN '-' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA, 
                            CASE WHEN UsuarioModificacion IS NULL THEN '-' ELSE UsuarioModificacion END AS USER_MODIFICA, Estado,ID_SCC 
                        FROM S_CentrosCostos 
                        WHERE (%s = 0 OR Abrev = %s) AND Estado = 'A'
                        ORDER BY Descripcion;
                    """, (centro,centro))
                    consulta = cursor.fetchall()
                    listado = []
                    if consulta:
                        for row in consulta:
                            idConcepto = str(row[0])
                            descripcion = str(row[1])
                            fechaAlta = str(row[2])
                            user = str(row[3])
                            fechaModifica = str(row[4])
                            userModifica = str(row[5])
                            estado = str(row[6])
                            idCC = str(row[7])
                            datos = {'Abrev': idConcepto, 'Descripcion': descripcion, 
                                     'Alta': fechaAlta, 'Usuario':user, 
                                     'FechaModifica':fechaModifica, 'UserModifica': userModifica, 'Estado':estado, 'ID':idCC}
                            listado.append(datos)
                        return JsonResponse({'Message': 'Success', 'Datos': listado})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    

@login_required
@csrf_exempt
def eliminaCentro(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.CC_Elimina')
        if user_has_permission:
            usuario = str(request.user).upper()
            idCentro = request.POST.get('Centro')
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_CentrosCostos SET  Estado = 'E', FechaBaja = NOW(), UsuarioBaja = %s
                            WHERE ID_SCC = %s 
                        """
                    cursor.execute(sql,(usuario,idCentro))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Centro se eliminó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
   
#################################### FINAL CENTROS COSTOS ####################################





#################################### INICIO LEGAJOS ####################################

@login_required
@csrf_exempt
def subirLegajos(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.L_Inserta')
        if user_has_permission:
            file = request.FILES.get('archivoJSON')
            try:
                if not file:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'Ocurrió un error al intentar importar los Legajos.'})
                data = json.load(file)
                for item in data:
                    try:
                        with connections['FEE'].cursor() as cursor:
                            sql = """
                                    INSERT INTO S_Legajos (IdLegajo, Apellidos, Nombres, TipoDocumento, Documento, FechaNac, Sexo, Cuil, AbrevCosto, Estado)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                                    ON DUPLICATE KEY UPDATE
                                        Apellidos = VALUES(Apellidos),
                                        Nombres = VALUES(Nombres),
                                        TipoDocumento = VALUES(TipoDocumento),
                                        Documento = VALUES(Documento),
                                        FechaNac = VALUES(FechaNac),
                                        Sexo = VALUES(Sexo),
                                        Cuil = VALUES(Cuil),
                                        AbrevCosto = VALUES(AbrevCosto),
                                        Estado = VALUES(Estado);

                                    """
                            cursor.execute(sql,[ 
                                   item["IdLegajo"], 
                                   item["Apellidos"], 
                                   item["Nombres"], 
                                   item["IdTipoDocumento"], 
                                   item["Documento"], 
                                   item["FechaNacimiento"], 
                                   item["Sexo"], 
                                   item["CUIL"], 
                                   item["IdCCosto"], 
                                   item["Estado"]])
                            connections['FEE'].commit()
                    except Exception as e:
                        error = str(e)
                        return JsonResponse({'Message': 'Error', 'Nota': error})
                    finally:
                        connections['FEE'].close()
                return JsonResponse({'Message': 'Success', 'Nota': 'Los Legajos de importaron correctamente.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

def listarCentrosLegajos(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                listado_centros = [{'IdAbrev': '0', 'Descripcion': 'TODOS'}]
                sql = """
                        SELECT Abrev AS ABREVIATURA, Descripcion AS CENTRO
                        FROM S_CentrosCostos
                        WHERE Estado = 'A'
                        ORDER BY Abrev, Descripcion
                        """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idAbrev = str(row[0])
                        descripcion = str(row[1])
                        datos = {'IdAbrev': idAbrev, 'Descripcion': descripcion}
                        listado_centros.append(datos)
                return JsonResponse({'Message': 'Success', 'Datos': listado_centros})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            cursor.close()
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@login_required
@csrf_exempt
def listarLegajos(request):
    if request.method == 'POST':
        try:
            idCentro = str(request.POST.get('idCentro'))
            with connections['FEE'].cursor() as cursor:
                listado = [{'Legajo': '0', 'Nombre': 'TODOS'}]
                sql = """
                        SELECT IdLegajo AS LEGAJO, Apellidos AS APELLIDO, Nombres AS NOMBRE
                        FROM S_Legajos
                        WHERE (%s = '0' OR AbrevCosto = %s ) AND Estado = 'A'
                        ORDER BY Apellidos
                        """
                cursor.execute(sql, (idCentro,idCentro))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[0]) + ' - ' + str(row[1]) + ' ' + str(row[2])
                        datos = {'Legajo': legajo, 'Nombre': nombre}
                        listado.append(datos)
                return JsonResponse({'Message': 'Success', 'Datos': listado})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def listarLegajosTabla(request):
    if request.method == 'POST':
        idLegajo = str(request.POST.get('IdLegajo'))
        Abrev = str(request.POST.get('Abrev'))
        try:
            with connections['FEE'].cursor() as cursor:
                listado = []
                sql = """
                        SELECT        S_Legajos.ID_L AS ID, S_Legajos.IdLegajo AS LEGAJO, CONCAT(S_Legajos.Apellidos, ' ', S_Legajos.Nombres) AS NOMBRE, S_Legajos.TipoDocumento AS TIPO, 
                                                S_Legajos.Documento AS DNI, DATE_FORMAT(FechaNac, '%%d/%%m/%%Y') AS F_NACIMIENTO, S_Legajos.Sexo AS SEXO, S_Legajos.AbrevCosto, S_CentrosCostos.Descripcion AS CENTRO
                        FROM            S_Legajos INNER JOIN
                                                S_CentrosCostos ON S_Legajos.AbrevCosto = S_CentrosCostos.Abrev
                        WHERE 
                            (
                                (%s = '0' AND %s = '0') 
                                OR (%s = '0' AND S_Legajos.AbrevCosto = %s)
                                OR (S_Legajos.IdLegajo = %s)
                                OR (S_Legajos.IdLegajo = %s AND S_Legajos.AbrevCosto = %s)
                            ) 
                            AND S_Legajos.Estado = 'A'
                        ORDER BY 
                            S_Legajos.Apellidos;
                        """
                cursor.execute(sql, (idLegajo,Abrev,idLegajo,Abrev,idLegajo,idLegajo,Abrev))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        legajo = str(row[1])
                        nombre = str(row[2])
                        tipo = str(row[3])
                        dni = str(row[4])
                        nac = str(row[5])
                        sexo = str(row[6])
                        abrev = str(row[7])
                        centro = str(row[8])
                        datos = {'Legajo': legajo, 'Nombre': nombre, 'Tipo': tipo, 'DNI': dni, 'Nac': nac, 'Sexo': sexo, 'Abrev': abrev, 'Centro': centro}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

#################################### FINAL LEGAJOS ####################################







#################################### INICIO ADICIONALES ####################################

@login_required
@csrf_exempt
def listarLegajosConceptos(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                legajos = []
                conceptos = []
                centros = []
                sqlLegajos = """
                        SELECT        S_Legajos.IdLegajo AS LEGAJO, CONCAT(S_Legajos.Apellidos, ' ', S_Legajos.Nombres, ' (',S_Legajos.AbrevCosto,')' ) AS NOMBRE, 
                                    CASE WHEN S_CentrosCostos.Descripcion IS NULL THEN '-' ELSE S_CentrosCostos.Descripcion END AS CENTRO, S_Legajos.AbrevCosto
                        FROM            S_Legajos LEFT JOIN
                                                S_CentrosCostos ON S_Legajos.AbrevCosto = S_CentrosCostos.Abrev
                        WHERE        (S_Legajos.Estado = 'A')
                        ORDER BY S_Legajos.Apellidos
                        """
                cursor.execute(sqlLegajos)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[0]) + ' - ' + str(row[1])
                        centro = str(row[2])
                        abrev = str(row[3])
                        datos = {'Legajo': legajo, 'Nombre': nombre, 'Centro':centro, 'Abrev': abrev}
                        legajos.append(datos)

                sqlConceptos = """
                        SELECT  ID_SC AS ID, Descripcion AS CONCEPTO
                        FROM S_Conceptos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlConceptos)
                consulta2 = cursor.fetchall()
                if consulta2:
                    for row in consulta2:
                        idConcepto = str(row[0])
                        descripcion = 'ID: ' + str(row[0]) + ' - ' + str(row[1])
                        datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion}
                        conceptos.append(datos)

                sqlCentros = """
                        SELECT  Abrev AS ABREV, Descripcion AS DESCRIPCION
                        FROM S_CentrosCostos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlCentros)
                consulta3 = cursor.fetchall()
                if consulta3:
                    for row in consulta3:
                        abrev = str(row[0])
                        centro = str(row[0]) + ' - ' + str(row[1])
                        datos = {'Abrev': abrev, 'Centro': centro}
                        centros.append(datos)

                if legajos and conceptos and centros:
                    return JsonResponse({'Message': 'Success', 'Legajos': legajos, 'Conceptos': conceptos, 'Centros':centros})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def guardaAdicional(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Inserta')
        if user_has_permission:
            legajo = str(request.POST.get('legajo'))
            concepto = str(request.POST.get('concepto'))
            abrev = str(request.POST.get('abrev'))
            fecha = str(request.POST.get('fecha'))
            importe = str(request.POST.get('importe'))
            detalle = str(request.POST.get('detalle')).upper()
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            INSERT INTO S_Adicionales (IdLegajo, IdConcepto, Fecha, Importe, Detalle, FechaAlta, Usuario, Estado, Abrev)
                            VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'P', %s)
                        """
                    cursor.execute(sql,(legajo,concepto,fecha,importe,detalle,usuario,abrev))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        sql2 = """ 
                            SELECT  ID_A AS ID
                            FROM S_Adicionales
                            WHERE IdLegajo = %s AND IdConcepto = %s AND Fecha = %s AND Importe = %sAND Detalle = %s AND Usuario = %s
                    
                            """
                        cursor.execute(sql2,(legajo,concepto,fecha,importe,detalle,usuario))
                        result = cursor.fetchone()
                        if result:
                            ID_A = str(result[0])
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Adicional se agregó correctamente.', 'ID': ID_A})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

@login_required
@csrf_exempt
def listarConceptosCentros(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                centros = [{'Abrev': '0', 'Centro':'TODOS'}]
                conceptos = [{'IdConcepto': '0', 'Descripcion': 'TODO'}]
                liquidaciones = []
                sqlCentros = """
                        SELECT Abrev AS ABREV, Descripcion AS CENTRO
                        FROM S_CentrosCostos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlCentros)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        Abrev = str(row[0])
                        centro = str(row[0]) + ' - ' + str(row[1])
                        datos = {'Abrev': Abrev, 'Centro':centro}
                        centros.append(datos)

                sqlConceptos = """
                        SELECT  ID_SC AS ID, Descripcion AS CONCEPTO
                        FROM S_Conceptos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlConceptos)
                consulta2 = cursor.fetchall()
                if consulta2:
                    for row in consulta2:
                        idConcepto = str(row[0])
                        descripcion = 'ID: ' + str(row[0]) + ' - ' + str(row[1])
                        datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion}
                        conceptos.append(datos)

                sqlLiquidacion = """
                        SELECT ID_L, Carpeta 
                        FROM S_Liquidaciones 
                        WHERE ID_L > 0 AND Estado = 'A'
                        ORDER BY FechaAlta DESC
                        """
                cursor.execute(sqlLiquidacion)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idLiquidacion = str(row[0])
                        liquidacion = str(row[1])
                        datos = {'IdLiquidacion': idLiquidacion, 'Liquidacion':liquidacion}
                        liquidaciones.append(datos)

                if centros and conceptos:
                    return JsonResponse({'Message': 'Success', 'Centros': centros, 'Conceptos': conceptos, 'Liquidaciones': liquidaciones})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@login_required
@csrf_exempt
def listarLegajosTablaMasiva(request):
    if request.method == 'POST':
        try:
            Abrev = str(request.POST.get('Abrev'))
            with connections['FEE'].cursor() as cursor:
                listado = []
                sql = """
                        SELECT IdLegajo AS LEGAJO, CONCAT(Apellidos, ' ', Nombres) AS NOMBRE, AbrevCosto
                        FROM S_Legajos 
                        WHERE (%s = '0' OR AbrevCosto = %s) AND Estado = 'A' 
                        ORDER BY Apellidos
                        """
                cursor.execute(sql, (Abrev,Abrev))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[2]) + ' - ' + str(row[1])
                        datos = {'Legajo': legajo, 'Nombre': nombre}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'Nor Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@login_required
@csrf_exempt
def guardaAdicionalMasivo(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Inserta')
        if user_has_permission:
            legajos = request.POST.getlist('legajos')
            concepto = str(request.POST.get('concepto'))
            abrev = str(request.POST.get('abrev'))
            fecha = str(request.POST.get('fecha'))
            importe = str(request.POST.get('importe'))
            detalle = str(request.POST.get('detalle')).upper()
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            INSERT INTO S_Adicionales (IdLegajo, IdConcepto, Fecha, Importe, Detalle, FechaAlta, Usuario, Estado, Abrev)
                            VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'P', %s)
                        """
                    for legajo in legajos:
                        cursor.execute(sql,(legajo,concepto,fecha,importe,detalle,usuario,abrev))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        sql2 = """ 

                            SELECT  MAX(ID_A) AS ID
                            FROM S_Adicionales
                    
                            """
                        cursor.execute(sql2)
                        result = cursor.fetchone()
                        if result:
                            ID_A = str(result[0])
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Adicional se agregó correctamente.', 'ID': ID_A})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})      

@login_required
@csrf_exempt
def listarConceptosCentrosEstado(request):
    if request.method == 'GET':
        try:
            with connections['FEE'].cursor() as cursor:
                centros = [{'Abrev': '0', 'Centro': 'TODOS'}]
                conceptos = [{'IdConcepto': '0', 'Descripcion': 'TODO'}]
                estados = [{'IDestado': '0', 'Estado': 'TODO'},{'IDestado': 'L', 'Estado': 'LIQUIDADO'},
                           {'IDestado': 'P', 'Estado': 'PENDIENTE'},{'IDestado': 'A', 'Estado': 'ANULADO'}]

                sqlCentros = """
                        SELECT Abrev AS ABREV, Descripcion AS CENTRO
                        FROM S_CentrosCostos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlCentros)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        Abrev = str(row[0])
                        centro = str(row[0]) + ' - ' + str(row[1])
                        datos = {'Abrev': Abrev, 'Centro':centro}
                        centros.append(datos)

                sqlConceptos = """
                        SELECT  ID_SC AS ID, Descripcion AS CONCEPTO
                        FROM S_Conceptos
                        WHERE Estado = 'A'
                        ORDER BY Descripcion
                        """
                cursor.execute(sqlConceptos)
                consulta2 = cursor.fetchall()
                if consulta2:
                    for row in consulta2:
                        idConcepto = str(row[0])
                        descripcion = str(row[1])
                        datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion}
                        conceptos.append(datos)
                if centros and conceptos:
                    return JsonResponse({'Message': 'Success', 'Centros': centros, 'Conceptos': conceptos, 'Estados':estados})
                else:
                    return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def listarAdicionalesTabla(request):
    if request.method == 'POST':
        inicio = str(request.POST.get('Inicio'))
        final = str(request.POST.get('Final'))
        centro = str(request.POST.get('Centro')) or '0'
        legajo = str(request.POST.get('Legajo')) or '0'
        concepto = str(request.POST.get('Concepto')) or '0'
        estadoInicial = str(request.POST.get('Estado')) or '0'
        cant = ""
        importe_total = ""
        color = ""
        try:
            with connections['FEE'].cursor() as cursor:
                listado = []
                sql = """
                        SELECT        S_Adicionales.ID_A AS ID, S_Adicionales.IdLegajo AS LEGAJO, CONCAT(S_Legajos.Apellidos,' ', S_Legajos.Nombres, ' - (',S_Legajos.AbrevCosto, ')') AS NOMBRE, S_CentrosCostos.Abrev AS ABREV, S_CentrosCostos.Descripcion AS CENTRO, 
                                                S_Adicionales.IdConcepto AS ID_CONCEPTO, S_Conceptos.Descripcion AS CONCEPTO, DATE_FORMAT(S_Adicionales.Fecha, '%%d/%%m/%%Y') AS FECHA, S_Adicionales.Importe AS IMPORTE, 
                                                DATE_FORMAT(S_Adicionales.FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, S_Adicionales.Usuario AS USUARIO, S_Adicionales.Estado,
                                                CASE S_Adicionales.Estado WHEN 'P' THEN 'PENDIENTE' WHEN 'L' THEN 'LIQUIDADO' WHEN 'A' THEN 'ANULADO' END AS ESTADO,
                                                CASE S_Adicionales.Estado WHEN 'P' THEN 'orange' WHEN 'L' THEN 'green' WHEN 'A' THEN 'red' END AS COLOR, CONCAT(S_Adicionales.Abrev, ' - ', (SELECT Descripcion FROM S_CentrosCostos WHERE Abrev = S_Adicionales.Abrev)),
                                                COUNT(*) OVER () AS TOTAL_ITEMS, SUM(S_Adicionales.Importe) OVER () AS TOTAL_IMPORTE
                        FROM            S_Adicionales INNER JOIN
                                                S_Legajos ON S_Adicionales.IdLegajo = S_Legajos.IdLegajo LEFT JOIN
                                                S_CentrosCostos ON S_Legajos.AbrevCosto = S_CentrosCostos.Abrev INNER JOIN
                                                S_Conceptos ON S_Adicionales.IdConcepto = S_Conceptos.ID_SC
                        WHERE       DATE(S_Adicionales.Fecha) >= %s
                                    AND DATE(S_Adicionales.Fecha) <= %s
                                    AND (%s = '0' OR S_CentrosCostos.Abrev = %s)
                                    AND (%s = '0' OR S_Adicionales.IdLegajo = %s)
                                    AND (%s = '0' OR S_Adicionales.IdConcepto = %s)
                                    AND (%s = '0' OR S_Adicionales.Estado = %s)
                                    AND S_Adicionales.Estado <> 'E'
                        ORDER BY S_Legajos.Apellidos, S_Adicionales.Fecha
                        
                        """
                cursor.execute(sql, (inicio,final,centro,centro,legajo,legajo,concepto,concepto,estadoInicial,estadoInicial))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idAdicional = str(row[0])
                        legajo = str(row[1])
                        nombre = str(row[2])
                        abrev = str(row[3])
                        centro = str(row[4])
                        idConcepto = str(row[5])
                        concepto = str(row[6])
                        fecha = str(row[7])
                        importe = str(row[8]).replace('.', ',')
                        alta = str(row[9])
                        usuario = str(row[10])
                        idEstado = str(row[11])
                        estado = str(row[12])
                        color = str(row[13])
                        abrev2 = str(row[14])
                        cant = str(row[15])
                        importe_total = formatear_numero(row[16])
                        datos = {'IdAdicional': idAdicional,'Legajo': legajo, 'Nombre': nombre, 'Abrev': abrev, 'Centro': centro,
                                 'IdConcepto': idConcepto, 'Concepto': concepto, 'Fecha': fecha, 'Importe': importe, 
                                 'Alta': alta, 'Usuario': usuario, 'IdEstado': idEstado, 'Estado': estado, 'Color': color, 'Abrev2': abrev2}
                        listado.append(datos)
                    if str(estadoInicial) == '0':
                        color = 'grey'
                    return JsonResponse({'Message': 'Success', 'Datos': listado, 'Cantidad':cant, 'Total':importe_total, 'Color':color})
                else:
                    return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def datosModificaAdicional(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Modifica')
        if user_has_permission:
            idAdicional = request.POST.get('IdAdicional')
            try:
                conceptos = []
                with connections['FEE'].cursor() as cursor:

                    sqlConceptos = """
                            SELECT  ID_SC AS ID, Descripcion AS CONCEPTO
                            FROM S_Conceptos
                            WHERE Estado = 'A'
                            ORDER BY Descripcion
                            """
                    cursor.execute(sqlConceptos)
                    consulta2 = cursor.fetchall()
                    if consulta2:
                        for row in consulta2:
                            idConcepto = str(row[0])
                            descripcion = str(row[1])
                            datos = {'IdConcepto': idConcepto, 'Descripcion': descripcion}
                            conceptos.append(datos)

                    sql = """ 
                            SELECT        S_Adicionales.ID_A AS ID, CONCAT(CAST(S_Adicionales.IdLegajo AS CHAR), ' - ', S_Legajos.Apellidos, ' ', S_Legajos.Nombres, ' (',S_Legajos.AbrevCosto,')') AS NOMBRE, CONCAT(S_Adicionales.Abrev, ' - ', (SELECT Descripcion FROM S_CentrosCostos WHERE Abrev = S_Adicionales.Abrev)) AS CENTRO, 
                                            DATE_FORMAT(S_Adicionales.Fecha, '%%Y-%%m-%%d') AS FECHA, S_Adicionales.Importe AS IMPORTE, S_Adicionales.Detalle AS DETALLE,
                                            S_Adicionales.IdConcepto AS ID_CONCEPTO
                            FROM            S_Adicionales INNER JOIN
                                                    S_Legajos ON S_Adicionales.IdLegajo = S_Legajos.IdLegajo LEFT JOIN
                                                    S_CentrosCostos ON S_Legajos.AbrevCosto = S_CentrosCostos.Abrev
                            WHERE        (S_Adicionales.ID_A = %s)
                        """
                    cursor.execute(sql,(idAdicional,))
                    consulta = cursor.fetchone()
                    if consulta:
                        IdAdicional = str(consulta[0])
                        nombre = str(consulta[1])
                        centro = str(consulta[2])
                        fecha = str(consulta[3])
                        importe = str(consulta[4])
                        detalle = str(consulta[5])
                        concepto = str(consulta[6])
                        return JsonResponse({'Message': 'Success', 'IdAdicional': IdAdicional, 'Nombre': nombre, 'Centro': centro, 'Fecha': fecha, 
                                             'Importe': importe, 'Detalle': detalle, 'IdConcepto': concepto, 'Conceptos': conceptos})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

@login_required
@csrf_exempt
def ActualizaAdicional(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Modifica')
        if user_has_permission:
            idAdicional = request.POST.get('IdAdicional')
            idConcepto = request.POST.get('IdConcepto')
            idFecha = request.POST.get('IdFecha')
            idImporte = request.POST.get('IdImporte') 
            idDetalle = request.POST.get('IdDetalle')
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Adicionales SET IdConcepto = %s, Fecha = %s, Importe = %s, Detalle = %s, FechaModificacion = NOW(), UsuarioModificacion = %s WHERE ID_A = %s
                        """
                    cursor.execute(sql,(idConcepto,idFecha,idImporte,idDetalle,usuario,idAdicional))
                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Adicional se actualizó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

@login_required
@csrf_exempt
def eliminaAdicional(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Elimina')
        if user_has_permission:
            idAdicional = request.POST.get('IdAdicional')
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Adicionales SET Estado = 'A', FechaBaja = NOW(), UsuarioBaja = %s WHERE ID_A = %s
                        """
                    cursor.execute(sql,(usuario,idAdicional))
                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]
                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Adicional se anuló correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   



#################################### FINAL ADICIONALES ####################################





#################################### INICIO LIQUIDACIONES ####################################


@login_required
@csrf_exempt
def guardaLiquidacion(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.LQ_Inserta')
        if user_has_permission:
            carpeta = str(request.POST.get('carpeta')).upper()
            estado = str(request.POST.get('estado'))
            usuario = str(request.user).upper()
            if verificaNombreLiquidacion(carpeta):
                return JsonResponse({'Message': 'Error', 'Nota': 'El nombre de la Liquidación ya existe.'})
            else:
                try:
                    with connections['FEE'].cursor() as cursor:
                        sql = """ 
                                INSERT INTO S_Liquidaciones (UsuarioImpresiones,Impresiones, Carpeta, FechaAlta, Usuario, Estado)
                                VALUES ('','0',%s, NOW(), %s, %s)
                            """
                        cursor.execute(sql,(carpeta,usuario,estado))

                        cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                        affected_rows = cursor.fetchone()[0]

                        if affected_rows > 0:
                            sql2 = """ 
                                SELECT  ID_L AS ID, Carpeta AS LIQUIDACION, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                                    CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA,
                                    CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA
                                FROM S_Liquidaciones
                                WHERE Carpeta = %s
                        
                                """
                            cursor.execute(sql2,(carpeta,))
                            result = cursor.fetchone()
                            if result:
                                ID_L = str(result[0])
                                fechaAlta = str(result[2])
                                usuario = str(result[3])
                                fechaMod = str(result[4])
                                usuarioMod = str(result[5])
                            return JsonResponse({'Message': 'Success', 'Nota': 'La Liquidación se creó correctamente.', 'ID': ID_L, 'FechaAlta': fechaAlta, 'Usuario': usuario, 'FechaModifica': fechaMod, 'UserModifica':usuarioMod})
                        else:
                            return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
                except Exception as e:
                    error = str(e)
                    return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
                finally:
                    connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

def verificaNombreLiquidacion(carpeta):
    try:
        with connections['FEE'].cursor() as cursor:
            sql = """ 
                    SELECT Carpeta FROM S_Liquidaciones WHERE Carpeta = %s
                """
            cursor.execute(sql,(carpeta,))

            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
    except Exception as e:
        return False
    finally:
        connections['FEE'].close()

def verificaNombreLiquidacionActualizacion(carpeta,idL):
    try:
        with connections['FEE'].cursor() as cursor:
            sql = """ 
                    SELECT Carpeta FROM S_Liquidaciones WHERE Carpeta = %s AND ID_L <> %s;
                """
            cursor.execute(sql,(carpeta,idL))

            result = cursor.fetchone()

            if result:
                return True
            else:
                return False
    except Exception as e:
        return False
    finally:
        connections['FEE'].close()

@login_required
@csrf_exempt
def listarLiquidacionesTabla(request):
    if request.method == 'POST':
        inicio = str(request.POST.get('Inicio'))
        final = str(request.POST.get('Final'))
        estado = str(request.POST.get('Estado')) or '0'
        try:
            with connections['FEE'].cursor() as cursor:
                listado = []
                sql = """
                        SELECT ID_L AS ID, Carpeta AS NOMBRE, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS FECHA, Usuario AS USUARIO,
                        CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS FMODIFICA,
                        CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS FMODIFICA,
                        CASE WHEN Estado = 'A' THEN 'ABIERTO' WHEN Estado = 'C' THEN 'CERRADO' WHEN Estado ='L' THEN 'LIQUIDADO' END AS ESTADO,
                        CASE WHEN Estado = 'A' THEN 'green' WHEN Estado = 'C' THEN 'red' WHEN Estado = 'L' THEN 'grey' END AS COLOR,
                        Estado AS LETRA
                        FROM `S_Liquidaciones`
                        WHERE DATE(FechaAlta) >= %s
                                AND DATE(FechaAlta) <= %s
                            AND (%s = '0' OR Estado = %s);
                        
                        """
                cursor.execute(sql, (inicio,final,estado,estado))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idL= str(row[0])
                        nombre = str(row[1])
                        fecha = str(row[2])
                        usuario = str(row[3])
                        fmodifica = str(row[4])
                        umodifica = str(row[5])
                        estado = str(row[6])
                        color = str(row[7])
                        letra = str(row[8])
                        datos = {'IdLiquidacion': idL, 'Nombre': nombre, 'Fecha': fecha, 'Usuario': usuario, 
                                 'FechaModifica': fmodifica, 'UsuarioModifica': umodifica, 'Estado': estado, 'Color': color, 'Letra': letra}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def datosModificaLiquidacion(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.LQ_Modifica')
        if user_has_permission:
            idLiquidacion = str(request.POST.get('IdLiquidacion'))
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            SELECT  ID_L AS ID, Carpeta AS LIQUIDACION, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i') AS ALTA, Usuario AS USUARIO, 
                                    CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA,
                                    CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA, Estado AS ESTADO, Liquidado AS LIQUIDADO,
                                    CASE Estado WHEN 'C' THEN 'red' WHEN 'A' THEN 'green' WHEN 'L' THEN 'grey' END AS COLOR,
                                    CASE Estado WHEN 'A' THEN 'ABIERTA' WHEN 'C' THEN 'CERRADA' WHEN 'L' THEN 'LIQUIDADA' END AS LETRAS
                                FROM S_Liquidaciones
                                WHERE ID_L = %s;
                        """
                    cursor.execute(sql,(idLiquidacion,))
                    consulta = cursor.fetchone()
                    if consulta:
                        IdLiquidacion = str(consulta[0])
                        nombre = str(consulta[1])
                        fechaAlta = str(consulta[2])
                        usuarioAlta = str(consulta[3])
                        fechaMod = str(consulta[4])
                        userMod = str(consulta[5])
                        estado = str(consulta[6])
                        color = str(consulta[8])
                        letras = str(consulta[9])
                        return JsonResponse({'Message': 'Success', 'IdLiquidacion': IdLiquidacion, 'Nombre': nombre, 'FechaAlta': fechaAlta, 'UsuarioAlta': usuarioAlta,
                                             'FechaModifica': fechaMod, 'UsuarioModifica': userMod, 'Estado': estado, 'Color': color,'Letras': letras})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    
@login_required
@csrf_exempt
def cierraLiquidacionMasivo(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.LQ_Modifica')
        if user_has_permission:
            liquidaciones = request.POST.getlist('liquidaciones')
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Liquidaciones SET Estado = 'C', UsuarioCierre = %s, FechaCierre = NOW() WHERE ID_L = %s;
                        """
                    for item in liquidaciones:
                        cursor.execute(sql,(usuario,item))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'Las Liquidaciones se cerraron correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})     
    
@login_required
@csrf_exempt
def actualizaLiquidacion(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.LQ_Modifica')
        permiso_apertura = request.user.has_perm('Salary.LQ_AbreLiqui')
        if user_has_permission:
            usuario = str(request.user).upper()
            id_L = request.POST.get('IdLiquidacion')
            estado = str(request.POST.get('Estado'))
            carpeta = str(request.POST.get('Carpeta')).upper()
            if str(retornaCantidadImpresiones(id_L)) == '0':
                if verificaNombreLiquidacionActualizacion(carpeta, id_L):
                    return JsonResponse({'Message': 'Error', 'Nota': 'El nombre de la Liquidación ya existe.'})
                else:
                    try:
                        with connections['FEE'].cursor() as cursor:
                            sql = """ 
                                    UPDATE S_Liquidaciones SET  Carpeta = %s, FechaModificacion = NOW(), UsuarioModificacion = %s, Estado = %s 
                                    WHERE ID_L = %s 
                                """
                            cursor.execute(sql,(carpeta,usuario,estado,id_L))

                            cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                            affected_rows = cursor.fetchone()[0]

                            if affected_rows > 0:
                                sql2 = """ 
                                    SELECT  ID_L, Carpeta, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i'), Usuario, 
                                            CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA,
                                            CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA, Estado AS ESTADO,
                                            CASE Estado WHEN 'C' THEN 'red' WHEN 'A' THEN 'green' WHEN 'L' THEN 'grey' END AS COLOR,
                                            CASE Estado WHEN 'A' THEN 'ABIERTA' WHEN 'C' THEN 'CERRADA' WHEN 'L' THEN 'LIQUIDADA' END AS LETRAS
                                    FROM S_Liquidaciones 
                                    WHERE ID_L = %s;
                                    """
                                cursor.execute(sql2,(id_L,))
                                result = cursor.fetchone()
                                if result:
                                    idLiquidacion = str(result[0])
                                    nombre = str(result[1])
                                    fechaAlta = str(result[2])
                                    usuarioAlta = str(result[3])
                                    fechaModifica = str(result[4])
                                    userModifica = str(result[5])
                                    estado = str(result[6])
                                    color = str(result[7])
                                    letras = str(result[8])
                                return JsonResponse({'Message': 'Success', 'Nota': 'El Concepto se actualizó correctamente.', 'IdLiquidacion': idLiquidacion, 'Nombre': nombre, 'FechaAlta': fechaAlta, 'UsuarioAlta': usuarioAlta,
                                            'FechaModifica': fechaModifica, 'UsuarioModifica': userModifica, 'Color': color, 'Estado': estado, 'Letras': letras})
                            else:
                                return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
                    except Exception as e:
                        error = str(e)
                        return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
                    finally:
                            connections['FEE'].close()
            else:
                if permiso_apertura:
                    if verificaNombreLiquidacionActualizacion(carpeta, id_L):
                        return JsonResponse({'Message': 'Error', 'Nota': 'El nombre de la Liquidación ya existe.'})
                    else:
                        try:
                            with connections['FEE'].cursor() as cursor:
                                sql = """ 
                                        UPDATE S_Liquidaciones SET  Carpeta = %s, FechaModificacion = NOW(), UsuarioModificacion = %s, Estado = %s 
                                        WHERE ID_L = %s 
                                    """
                                cursor.execute(sql,(carpeta,usuario,estado,id_L))

                                cursor.execute("SELECT ROW_COUNT() AS AffectedRows;")
                                affected_rows = cursor.fetchone()[0]

                                if affected_rows > 0:
                                    sql2 = """ 
                                        SELECT  ID_L, Carpeta, DATE_FORMAT(FechaAlta, '%%d/%%m/%%Y %%H:%%i'), Usuario, 
                                                CASE WHEN FechaModificacion IS NULL THEN '' ELSE DATE_FORMAT(FechaModificacion, '%%d/%%m/%%Y %%H:%%i') END AS MODIFICA,
                                                CASE WHEN UsuarioModificacion IS NULL THEN '' ELSE UsuarioModificacion END AS USER_MODIFICA, Estado AS ESTADO,
                                                CASE Estado WHEN 'C' THEN 'red' WHEN 'A' THEN 'green' WHEN 'L' THEN 'grey' END AS COLOR,
                                                CASE Estado WHEN 'A' THEN 'ABIERTA' WHEN 'C' THEN 'CERRADA' WHEN 'L' THEN 'LIQUIDADA' END AS LETRAS
                                        FROM S_Liquidaciones 
                                        WHERE ID_L = %s;
                                        """
                                    cursor.execute(sql2,(id_L,))
                                    result = cursor.fetchone()
                                    if result:
                                        idLiquidacion = str(result[0])
                                        nombre = str(result[1])
                                        fechaAlta = str(result[2])
                                        usuarioAlta = str(result[3])
                                        fechaModifica = str(result[4])
                                        userModifica = str(result[5])
                                        estado = str(result[6])
                                        color = str(result[7])
                                        letras = str(result[8])
                                    return JsonResponse({'Message': 'Success', 'Nota': 'El Concepto se actualizó correctamente.', 'IdLiquidacion': idLiquidacion, 'Nombre': nombre, 'FechaAlta': fechaAlta, 'UsuarioAlta': usuarioAlta,
                                                'FechaModifica': fechaModifica, 'UsuarioModifica': userModifica, 'Color': color, 'Estado': estado, 'Letras': letras})
                                else:
                                    return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
                        except Exception as e:
                            error = str(e)
                            return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
                        finally:
                            connections['FEE'].close()
                else:
                    return JsonResponse ({'Message': 'Not Found', 'Nota': 'SIN PERMISOS: El Memorandum ya fue impreso, se requiere un super usuario o permisos especiales para abrir la Liquidacion.'})
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    

def retornaCantidadImpresiones(liquidacion):
    cantidad = '0'
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """ SELECT Impresiones FROM S_Liquidaciones WHERE ID_L = %s AND Estado IN ('A','C') """
            cursor.execute(sql2, (liquidacion,))
            consulta = cursor.fetchone()
            if consulta:
                cantidad = str(consulta[0])
                return cantidad
            else:
                return cantidad
    except Exception as e:
        error = str(e)
        return cantidad
    finally:
        connections['FEE'].close()

#################################### FINAL LIQUIDACIONES ####################################




#################################### INICIO PAGOS ####################################

@login_required
@csrf_exempt
def asignaLiquidaciones(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Inserta')
        if user_has_permission:
            adicionales = request.POST.getlist('adicionales')
            liquidacion = request.POST.get('liquidacion')
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Adicionales SET  IdLiquidacion = %s, Estado = 'L'
                            WHERE ID_A = %s
                        """
                    for item in adicionales:
                        cursor.execute(sql,(liquidacion,item))

                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'Los Adicionales se liquidaron correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})     

@login_required
@csrf_exempt
def listarLiquidacionesId(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Ingresa')
        if user_has_permission:
            inicio = str(request.POST.get('Inicio'))
            final = str(request.POST.get('Final'))
            try:
                with connections['FEE'].cursor() as cursor:
                    listado = []
                    sql = """
                            SELECT ID_L AS ID, Carpeta AS LIQUIDACION 
                            FROM S_Liquidaciones L
                            WHERE DATE(L.FechaAlta) >= %s
                            AND DATE(L.FechaAlta) <= %s AND Estado ='A'
                            AND EXISTS (
                                SELECT 1 
                                FROM S_Adicionales A 
                                WHERE A.IdLiquidacion = L.ID_L
                            );
                            
                            """
                    cursor.execute(sql, (inicio,final))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            idLiquidacion = str(row[0])
                            liquidacion = str(row[1])
                            datos = {'IdLiquidacion': idLiquidacion,'Liquidacion': liquidacion}
                            listado.append(datos)
                        return JsonResponse({'Message': 'Success', 'Liquidaciones': listado})
                    else:
                        return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    
@login_required
@csrf_exempt
def listarLiquidacionesIdImprimir(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Ingresa')
        if user_has_permission:
            inicio = str(request.POST.get('Inicio'))
            final = str(request.POST.get('Final'))
        
            try:
                with connections['FEE'].cursor() as cursor:
                    listado = []
                    sql = """
                            SELECT ID_L AS ID, Carpeta AS LIQUIDACION 
                            FROM S_Liquidaciones L
                            WHERE DATE(L.FechaAlta) >= %s
                            AND DATE(L.FechaAlta) <= %s AND Estado ='C'
                            AND EXISTS (
                                SELECT 1 
                                FROM S_Adicionales A 
                                WHERE A.IdLiquidacion = L.ID_L
                            );
                            """
                    cursor.execute(sql, (inicio,final))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            idLiquidacion = str(row[0])
                            liquidacion = str(row[1])
                            datos = {'IdLiquidacion': idLiquidacion,'Liquidacion': liquidacion}
                            listado.append(datos)
                        return JsonResponse({'Message': 'Success', 'Liquidaciones': listado})
                    else:
                        return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 
    
@login_required
@csrf_exempt
def listarCentrosLegajosP(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Ingresa')
        if user_has_permission:
            idLiquidacion = str(request.POST.get('IdLiquidacion'))
            try:
                with connections['FEE'].cursor() as cursor:
                    centros = [{'Abrev': '0','Centro': 'TODO'}]
                    personal = [{'Legajo': '0','Nombre': 'TODO'}]

                    sql = """
                            SELECT DISTINCT A.IdLegajo AS LEGAJO, CONCAT(L.Apellidos, ' ', L.Nombres) AS NOMBRES, L.Apellidos
                            FROM S_Adicionales A INNER JOIN 
                                    S_Legajos L ON A.IdLegajo = L.IdLegajo
                            WHERE A.IdLiquidacion = %s
                            ORDER BY L.Apellidos;
                            """
                    cursor.execute(sql, (idLiquidacion,))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            idLegajo = str(row[0])
                            nombre = str(row[0]) + ' - ' + str(row[1])
                            datos = {'Legajo': idLegajo,'Nombre': nombre}
                            personal.append(datos)
                    
                    sql2 = """
                            SELECT DISTINCT AbrevCosto AS ABREV, C.Descripcion AS CENTRO
                            FROM S_Legajos LE INNER JOIN
                                S_CentrosCostos C ON LE.AbrevCosto = C.Abrev
                            WHERE IdLegajo IN (
                                    SELECT DISTINCT A.IdLegajo
                                FROM S_Adicionales A INNER JOIN 
                                S_Legajos L ON A.IdLegajo = L.IdLegajo
                                WHERE A.IdLiquidacion = %s		
                            )
                            ORDER BY C.Descripcion;                          
                            """
                    cursor.execute(sql2, (idLiquidacion,))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            abrev = str(row[0])
                            descripcion = str(row[1])
                            datos = {'Abrev': abrev,'Centro': descripcion}
                            centros.append(datos)
                            
                    if centros and personal:
                        return JsonResponse({'Message': 'Success', 'Legajos': personal, 'Centros': centros})
                    else:
                        return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   

@login_required
@csrf_exempt
def listarDataLiquidacionesTabla(request):
    if request.method == 'POST':
        liquidacion = str(request.POST.get('Liquidacion'))
        centro = str(request.POST.get('Centro')) or '0'
        legajo = str(request.POST.get('Legajo')) or '0'
        try:
            with connections['FEE'].cursor() as cursor:
                listado = []
                sql = """
                        SELECT        S_Adicionales.ID_A AS ID, S_Adicionales.IdLegajo AS LEGAJO, CONCAT(S_Legajos.Apellidos,' ', S_Legajos.Nombres, ' - (', S_Legajos.AbrevCosto, ')') AS NOMBRE, 
                                        S_CentrosCostos.Abrev AS ABREV, S_CentrosCostos.Descripcion AS CENTRO, S_Conceptos.Descripcion AS CONCEPTO, 
                                        DATE_FORMAT(S_Adicionales.Fecha, '%%d/%%m/%%Y') AS FECHA, S_Adicionales.Importe AS IMPORTE, S_Adicionales.Detalle AS DETALLE, CONCAT(S_Adicionales.Abrev, ' - ', (SELECT Descripcion FROM S_CentrosCostos WHERE Abrev = S_Adicionales.Abrev))
                        FROM            S_Adicionales INNER JOIN
                                                S_Legajos ON S_Adicionales.IdLegajo = S_Legajos.IdLegajo LEFT JOIN
                                                S_CentrosCostos ON S_Legajos.AbrevCosto = S_CentrosCostos.Abrev INNER JOIN
                                                S_Conceptos ON S_Adicionales.IdConcepto = S_Conceptos.ID_SC
                        WHERE       S_Adicionales.IdLiquidacion = %s
                                    AND (%s = '0' OR S_CentrosCostos.Abrev = %s)
                                    AND (%s = '0' OR S_Adicionales.IdLegajo = %s)
                                    AND S_Adicionales.Estado <> 'E'
                        ORDER BY S_Legajos.Apellidos;
                        
                        """
                cursor.execute(sql, (liquidacion,centro,centro,legajo,legajo))
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        idAdicional = str(row[0])
                        legajo = str(row[1])
                        nombre = str(row[2])
                        abrev = str(row[3])
                        centro = str(row[3]) + ' - ' + str(row[4])
                        concepto = str(row[5])
                        fecha = str(row[6])
                        importe = str(row[7]).replace('.', ',')
                        detalle = str(row[8])
                        abrev2 = str(row[9])
                        datos = {'IdAdicional': idAdicional,'Legajo': legajo, 'Nombre': nombre, 'Abrev': abrev, 'Centro': centro,
                                 'Concepto': concepto, 'Fecha': fecha, 'Importe': importe, 
                                 'Detalle': detalle, 'Abrev2':abrev2}
                        listado.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': listado})
                else:
                    return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['FEE'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@login_required
@csrf_exempt
def quitaDeLiquidaciones(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Elimina')
        if user_has_permission:
            idAdicional = request.POST.get('IdAdicional')
            usuario = str(request.user).upper()
            try:
                with connections['FEE'].cursor() as cursor:
                    sql = """ 
                            UPDATE S_Adicionales SET  IdLiquidacion = NULL, Estado = 'P', FechaModificacion = NOW(), UsuarioModificacion = %s
                            WHERE ID_A = %s
                        """
                    cursor.execute(sql,(usuario,idAdicional))
                    cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
                    affected_rows = cursor.fetchone()[0]

                    if affected_rows > 0:
                        return JsonResponse({'Message': 'Success', 'Nota': 'El Adicional se quitó correctamente.'})
                    else:
                        return JsonResponse({'Message': 'Error', 'Nota': 'No se pudo resolver la petición.'})
            except Exception as e:
                error = str(e)
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})  
    
# def formatear_numero(numero):
#     locale.setlocale(locale.LC_ALL, 'es_ES.UTF-8')
#     numero_formateado = locale.format_string("%.2f", numero, grouping=True)
#     return f"$ {numero_formateado}"

# def formatear_numero(numero):
#     try:
#         numero_formateado = f"${numero:,.2f}"
#         numero_formateado = numero_formateado.replace(",", "X").replace(".", ",").replace("X", ".")
#         return numero_formateado
#     except (ValueError, TypeError):
#         return str(numero)
    
def formatear_numero(numero):
    try:
        numero = float(numero)
        numero_formateado = f"${numero:,.2f}"
        numero_formateado = numero_formateado.replace(",", "X").replace(".", ",").replace("X", ".")
        return numero_formateado
    except (ValueError, TypeError):
        return str(numero)

@login_required
@csrf_exempt
def listarCentrosCantidadImporte(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Ingresa')
        if user_has_permission:
            idLiquidacion = str(request.POST.get('Liquidacion'))
            try:
                with connections['FEE'].cursor() as cursor:
                    listado = []
                    sql = """
                            SELECT 
                                A.Abrev AS ABREV, 
                                C.Descripcion AS CENTRO, 
                                COUNT(*) AS CANTIDAD,
                                SUM(A.Importe) AS SUMA
                            FROM 
                                S_Adicionales A
                            INNER JOIN 
                                S_Legajos LE ON A.IdLegajo = LE.IdLegajo
                            INNER JOIN 
                                S_CentrosCostos C ON A.Abrev = C.Abrev
                            WHERE 
                                A.IdLiquidacion = %s
                            GROUP BY 
                                A.Abrev, C.Descripcion
                            ORDER BY 
                                C.Descripcion;
                                                        """
                    cursor.execute(sql, (idLiquidacion,))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            idCentro = str(row[0])
                            centro = str(row[0])
                            cantidad = str(row[2])
                            importe = formatear_numero(row[3])
                            datos = {'Abrev': idCentro,'Centro': centro, 'Cantidad': cantidad, 'Importe':importe}
                            listado.append(datos)
                                                
                    if listado:
                        return JsonResponse({'Message': 'Success', 'Datos': listado})
                    else:
                        return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    
@login_required
@csrf_exempt
def listarItemsCantidadImporte(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.P_Ingresa')
        if user_has_permission:
            idLiquidacion = str(request.POST.get('Liquidacion'))
            centros = request.POST.getlist('Centros')
            centros_str = ', '.join([f"'{centro}'" for centro in centros])
            #print(idLiquidacion)
            try:
                with connections['FEE'].cursor() as cursor:
                    listado = []
                    sql = f"""
                            SELECT 
                                A.IdLegajo AS LEGAJO, 
                                CONCAT(L.Apellidos, ' ', L.Nombres, ' (', L.AbrevCosto, ')') AS NOMBRES, 
                                CONCAT(C.Descripcion, ' (', C.Abrev,')') AS CENTRO, 
                                COUNT(A.ID_A) AS CANTIDAD_ADICIONALES,
                                SUM(A.Importe) AS TOTAL_IMPORTE,
                                A.Abrev
                            FROM 
                                S_Adicionales A 
                            INNER JOIN 
                                S_Legajos L ON A.IdLegajo = L.IdLegajo 
                            LEFT JOIN 
                                S_CentrosCostos C ON A.Abrev = C.Abrev
                            WHERE 
                                A.IdLiquidacion = %s 
                                AND A.Abrev IN ({centros_str})
                                AND A.Estado = 'L'
                            GROUP BY 
                                A.IdLegajo, 
                                L.Apellidos, 
                                L.Nombres, 
                                L.AbrevCosto, 
                                C.Descripcion,
                                C.Abrev,
                                A.Abrev
                            ORDER BY 
                                CONCAT(L.Apellidos, ' ', L.Nombres);

                            """
                    cursor.execute(sql, (idLiquidacion,))
                    consulta = cursor.fetchall()
                    if consulta:
                        for row in consulta:
                            legajo = str(row[0])
                            nombre = str(row[1])
                            centro = str(row[2])
                            cantidad = str(row[3])
                            importe = formatear_numero(row[4])
                            abrev = str(row[5])
                            datos = {'Legajo': legajo, 'Nombre': nombre,'Centro': centro, 'Cantidad': cantidad, 'Importe':importe, 'Abrev': abrev}
                            listado.append(datos)

                    sql1 = f""" SELECT COUNT(*) FROM S_Adicionales A INNER JOIN S_Legajos L ON A.IdLegajo = L.IdLegajo WHERE IdLiquidacion = %s AND A.Abrev IN ({centros_str}); """
                    cursor.execute(sql1, (idLiquidacion,))
                    consulta = cursor.fetchone()
                    if consulta:
                        cantidadTotal = str(consulta[0])  

                    sql2 = f""" SELECT SUM(Importe) FROM S_Adicionales A INNER JOIN S_Legajos L ON A.IdLegajo = L.IdLegajo WHERE IdLiquidacion = %s AND A.Abrev IN ({centros_str}); """
                    cursor.execute(sql2, (idLiquidacion,))
                    consulta = cursor.fetchone()
                    if consulta:
                        importeTotal = formatear_numero(consulta[0])

                    if listado:
                        return JsonResponse({'Message': 'Success', 'Datos': listado, 
                                             'CantTotal': cantidadTotal, 'ImporTotal': importeTotal})
                    else:
                        return JsonResponse({'Message': 'NotFound', 'Nota': 'No se encontraron datos.'})
            except Exception as e:
                error = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': error})
            finally:
                connections['FEE'].close()
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    
    

#################################### FINAL PAGOS  ####################################

#################################### INICIO IMPORTACIONES  ####################################



def clean_detail(detail):
    return re.sub(r'\s+', ' ', detail.strip())

@login_required
@csrf_exempt
def subirAdicionales(request):
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Salary.A_Inserta')
        usuario = str(request.user).upper()
        if user_has_permission:
            file = request.FILES.get('excel')
            if existeArchivo(str(file)):
                return JsonResponse({'Message': 'Duplicado', 'Nota': 'El archivo *' + str(file) + '* ya se importó, para evitar adicionales duplicados es necesario que verifique el contenido y/o cambie el nombre al archivo para poder volver a importar.'})
            else:
                if not file:
                    return JsonResponse ({'Message': 'Not Found', 'Nota': 'No se ha enviado ningún archivo'})
                try:
                    df = pd.read_excel(file)
                    num_filas = len(df)
                    required_columns = ['Legajo', 'Centro', 'Concepto', 'Fecha', 'Importe', 'Detalle']
                    if not all(column in df.columns for column in required_columns):
                        return JsonResponse ({'Message': 'Not Found', 'Nota': 'El archivo no tiene las columnas requeridas.'})                    
                    if not df['Legajo'].apply(lambda x: str(x).isdigit()).all():
                        return JsonResponse({'Message': 'Invalid Data', 'Nota': 'La columna Legajo contiene valores no numéricos.'})
                    if not df['Importe'].apply(lambda x: str(x).replace('.', '', 1).isdigit()).all():
                        return JsonResponse({'Message': 'Invalid Data', 'Nota': 'La columna Importe contiene valores no numéricos.'})
                    if not df['Concepto'].apply(lambda x: str(x).isdigit()).all():
                        return JsonResponse({'Message': 'Invalid Data', 'Nota': 'La columna Concepto contiene valores no numéricos.'})
                    try:
                        pd.to_datetime(df['Fecha'], format='%Y-%m-%d', errors='raise')
                    except ValueError:
                        return JsonResponse({'Message': 'Invalid Data', 'Nota': 'La columna Fecha contiene valores no válidos.'})
                    df['Fecha'] = pd.to_datetime(df['Fecha']).dt.date
                    df['Detalle'] = df['Detalle'].apply(clean_detail)
                    contador = 0
                    for index, row in df.iterrows():
                        #print(f"Legajo: {row['Legajo']}, Abrev: {row['Abrev']}, Concepto: {row['Concepto']}, Fecha: {row['Fecha']}, Importe: {row['Importe']}, Detalle: {row['Detalle']}")
                        if insertaAdicionalExcel(row['Legajo'],row['Concepto'],row['Fecha'],row['Importe'],row['Detalle'],usuario,row['Centro']):
                            contador = contador + 1
                    if contador == num_filas:
                        archivo = str(file).split('.')
                        insertaNombreArchivo(usuario,archivo[0],archivo[1])
                        return JsonResponse({'Message': 'Success', 'Nota': 'Los Adicionales se procesaron correctamente.'})
                    else:
                        archivo = str(file).split('.')
                        insertaNombreArchivo(usuario,archivo[0],archivo[1])
                        return JsonResponse({'Message': 'Error', 'Nota': 'Hubo un error al procesar ciertos adicionales.'})
                except Exception as e:
                    error = str(e)
                    return JsonResponse({'Message': 'Error', 'Nota': error})
        else:
            return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


#################################### FINAL IMPORTACIONES  ####################################



def insertaAdicionalExcel(legajo,concepto,fecha,importe,detalle,usuario,abrev):
    try:
        with connections['FEE'].cursor() as cursor:
            sql = """ 
                    INSERT INTO S_Adicionales (IdLegajo, IdConcepto, Fecha, Importe, Detalle, FechaAlta, Usuario, Estado, Abrev)
                    VALUES (%s, %s, %s, %s, %s, NOW(), %s, 'P', %s)
                """
            
            cursor.execute(sql,(legajo,concepto,fecha,importe,detalle,usuario,abrev))

            cursor.execute("SELECT ROW_COUNT() AS AffectedRows")
            affected_rows = cursor.fetchone()[0]

            if affected_rows > 0:
                sql2 = """ 

                    SELECT  MAX(ID_A) AS ID
                    FROM S_Adicionales
            
                    """
                cursor.execute(sql2)
                result = cursor.fetchone()
                if result:
                    ID_A = str(result[0])
                return True
            else:
                return False
    except Exception as e:
        error = str(e)
        return False
    finally:
        connections['FEE'].close()

def insertaNombreArchivo(usuario, archivo,tipo):
    try:
        with connections['FEE'].cursor() as cursor:
            sql = """ 
                    INSERT INTO S_Archivos (NombreArchivo, TipoArchivo, FechaAlta, Usuario)
                    VALUES (%s, %s, NOW(), %s)
                """
            cursor.execute(sql,(archivo,tipo,usuario))

    except Exception as e:
        error = str(e)
    finally:
        connections['FEE'].close()

def existeArchivo(archivo):
    try:
        with connections['FEE'].cursor() as cursor:
            sql = """ 
                    SELECT CONCAT(NombreArchivo, '.', TipoArchivo) AS ARCHIVO
                    FROM S_Archivos
                    HAVING ARCHIVO = %s;
                """
            cursor.execute(sql,(archivo,))
            results = cursor.fetchone()
            if results:
                return True
            else:
                return False
    except Exception as e:
        error = str(e)
        return True
    finally:
        connections['FEE'].close()

# CREATE TABLE S_Archivos (
#     ID INT AUTO_INCREMENT PRIMARY KEY,
#     NombreArchivo VARCHAR(255),
#     TipoArchivo VARCHAR(20),
#     FechaAlta DATETIME,
#     Usuario VARCHAR(255)
# );



















# def fechaString():
#     locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
#     fecha_formateada = datetime.now().strftime('%A %d de %B %Y')
#     partes_fecha = fecha_formateada.split(' ')
#     dia_semana = partes_fecha[0].capitalize()
#     dia = partes_fecha[1]
#     de = partes_fecha[2]
#     mes = partes_fecha[3].capitalize()
#     anio = partes_fecha[4]
#     fecha_capitalizada = f"{dia_semana} {dia} {de} {mes} del {anio}"
#     return fecha_capitalizada

def fechaString():
    dias_semana = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
    ahora = datetime.now()
    dia_semana = dias_semana[ahora.weekday()]
    dia = ahora.day
    mes = meses[ahora.month - 1]
    anio = ahora.year
    fecha_capitalizada = f"{dia_semana.capitalize()} {dia} de {mes} del {anio}"
    return fecha_capitalizada

def calcular_billetes(numero):
    denominaciones = [1000, 500, 200, 100, 50, 20, 10]
    billetes = {}
    importe_total = 0
    
    for denominacion in denominaciones:
        cantidad = numero // denominacion
        if cantidad > 0:
            billetes[denominacion] = {
                "cantidad": int(cantidad),
                "importe_parcial": int(cantidad) * denominacion
            }
            importe_total += int(cantidad) * denominacion
        numero %= denominacion

    resultado = {
        "billetes": billetes,
        "importe_total": importe_total
    }

    return resultado

def calcular_billetes_legajo(numero):
    denominaciones = [1000, 500, 200, 100, 50, 20, 10]
    billetes = {}
    importe_total = 0
    
    for denominacion in denominaciones:
        cantidad = numero // denominacion
        if cantidad > 0:
            billetes[denominacion] = {
                "cantidad": int(cantidad),
                "importe_parcial": int(cantidad) * denominacion
            }
            importe_total += int(cantidad) * denominacion
        numero %= denominacion

    resultado = {
        "billetes": billetes
    }

    return resultado

@login_required
@csrf_exempt
def imppresiones(request):
    if request.method == 'POST':
        codigo = str(request.POST.get('Codigo'))
        liquidacion = str(request.POST.get('Liquidacion'))
        centros = request.POST.getlist('Centros')
        lista = request.POST.getlist('Legajo') or ''
        if lista == [''] :
            lista = listaLegajos(liquidacion,centros)

        usuario = str(request.user).upper()
        centros_str = ', '.join([f"'{centro}'" for centro in centros])
        if codigo == 'M':
            user_has_permission = request.user.has_perm('Salary.I_Memo')
            if user_has_permission:
                nombres = str(request.user.last_name).upper() + ' ' + str(request.user.first_name).upper()
                try:
                    with connections['FEE'].cursor() as cursor:
                        sql2 = f""" SELECT SUM(Importe), S.Carpeta
                                    FROM S_Adicionales A INNER JOIN 
                                        S_Legajos L ON A.IdLegajo = L.IdLegajo INNER JOIN 
                                        S_Liquidaciones S ON A.IdLiquidacion = S.ID_L
                                    WHERE IdLiquidacion = %s AND A.Abrev IN ({centros_str}) """
                        cursor.execute(sql2, (liquidacion,))
                        consulta = cursor.fetchone()
                        if consulta:
                            numero = consulta[0]
                            importeTotal = formatear_numero(consulta[0])
                            nombreLiquidacion = str(consulta[1])

                        pdf = Memorandum(nombres,nombreLiquidacion,importeTotal)
                        pdf.alias_nb_pages()
                        pdf.add_page()

                        # pdf.set_fill_color(186, 233, 175)
                        # pdf.set_font('Arial', 'B', 12)
                        # pdf.multi_cell(w=0, h=6, txt= 'TOTAL CANTIDAD BILLETES', border='B', align='C', fill=False)
                        # pdf.multi_cell(w=0, h=3, txt= '', border='', align='C', fill=False)
                        # pdf.cell(w=60, h=6, txt= 'BILLETE', border='TLB', align='C', fill=True)
                        # pdf.cell(w=70, h=6, txt= 'CANTIDAD', border='TLB', align='C', fill=True)
                        # pdf.multi_cell(w=0, h=6, txt= 'IMPORTE', border='TLBR', align='C', fill=True)
                        
                        # billetes_acumulados = {}
                        # for legajo_r in lista:
                        #     datos = detallesItems(legajo_r,liquidacion)
                        #     datos_json = json.loads(datos)
                        #     totalSin = datos_json["total_sin"]
                        #     datas = calcular_billetes_legajo(float(totalSin))
                        #     billetes = datas["billetes"]
                        #     for denominacion, datos in billetes.items():
                        #         if denominacion not in billetes_acumulados:
                        #             billetes_acumulados[denominacion] = {
                        #                 "cantidad": 0,
                        #                 "importe_parcial": 0
                        #             }
                        #         billetes_acumulados[denominacion]["cantidad"] += datos["cantidad"]
                        #         billetes_acumulados[denominacion]["importe_parcial"] += datos["importe_parcial"]

                        # billetes_acumulados_json = json.dumps(billetes_acumulados, indent=4)
                        # billetes = json.loads(billetes_acumulados_json)
                        # for denominacion, info in billetes.items():
                        #     cantidad = info["cantidad"]
                        #     importe_parcial = info["importe_parcial"]
                        #     pdf.set_font('Arial', '', 10)
                        #     pdf.cell(w=60, h=6, txt= '$ ' + str(denominacion), border='LBR', align='C', fill=False)
                        #     pdf.cell(w=70, h=6, txt= str(cantidad), border='BR', align='C', fill=False)
                        #     pdf.multi_cell(w=0, h=6, txt= formatear_numero(importe_parcial), border='BR', align='C', fill=False)
                        # pdf.multi_cell(w=0, h=10, txt= '', border='', align='C', fill=False)

                        sql = f"""
                            SELECT 
                                A.Abrev AS ABREV, C.Descripcion AS CENTRO, COUNT(*) AS CANTIDAD, SUM(A.Importe) AS SUMA
                            FROM S_Adicionales A INNER JOIN 
                                S_Legajos LE ON A.IdLegajo = LE.IdLegajo INNER JOIN 
                                S_CentrosCostos C ON A.Abrev = C.Abrev
                            WHERE 
                                A.IdLiquidacion = %s AND A.Abrev IN ({centros_str})
                            GROUP BY 
                                A.Abrev, C.Descripcion
                            ORDER BY 
                                C.Descripcion
                            """
                        cursor.execute(sql, (liquidacion,))
                        consulta = cursor.fetchall()
                        if consulta:
                            # pdf.set_fill_color(186, 233, 175)
                            # pdf.set_font('Arial', 'B', 12)
                            # pdf.cell(w=130, h=6, txt= 'CENTRO DE COSTO', border='TLB', align='C', fill=True)
                            # pdf.multi_cell(w=0, h=6, txt= 'IMPORTE', border='TLBR', align='C', fill=True)
                            #print(lista)
                            for i in consulta:
                                pdf.set_fill_color(186, 233, 175)
                                pdf.set_font('Arial', 'B', 12)
                                pdf.cell(w=130, h=6, txt= 'CENTRO DE COSTO', border='TLB', align='C', fill=True)
                                pdf.multi_cell(w=0, h=6, txt= 'IMPORTE', border='TLBR', align='C', fill=True)
                                centro = str(i[1])
                                importeCentro = formatear_numero(i[3])
                                pdf.set_font('Arial', '', 10)
                                pdf.cell(w=130, h=7, txt= centro + ' - (' + str(i[0]) + ')', border='LBR', align='L', fill=False)
                                pdf.multi_cell(w=0, h=7, txt= importeCentro, border='BR', align='C', fill=False)
                                ####### INICIO PARTE NUEVA #######
                                
                                billetes_detalle = detallesItemsConCentro(str(i[0]),liquidacion,lista)
                                datos = json.loads(billetes_detalle)
                                billetes = datos["billetes_acumulados"]
                                pdf.set_font('Arial', 'B', 8)
                                pdf.multi_cell(w=0, h=1, txt= '', border='', align='C', fill=False)
                                pdf.cell(w=100, h=6, txt= '', border='', align='C', fill=False)
                                pdf.cell(w=30, h=4, txt= 'BILLETE', border='TLB', align='C', fill=True)
                                pdf.cell(w=30, h=4, txt= 'CANTIDAD', border='TLB', align='C', fill=True)
                                pdf.multi_cell(w=0, h=4, txt= 'IMPORTE', border='TLBR', align='C', fill=True)
                                
                                for denominacion, info in billetes.items():
                                    cantidad = info["cantidad"]
                                    importe_parcial = info["importe_parcial"]
                                    pdf.set_font('Arial', '', 8)
                                    pdf.cell(w=100, h=6, txt= '', border='', align='C', fill=False)
                                    pdf.cell(w=30, h=4, txt= '$ ' + str(denominacion), border='LBR', align='C', fill=False)
                                    pdf.cell(w=30, h=4, txt= str(cantidad), border='BR', align='C', fill=False)
                                    pdf.multi_cell(w=0, h=4, txt= formatear_numero(importe_parcial), border='BR', align='C', fill=False)
                                ####### FIN PARTE NUEVA #######
                                pdf.multi_cell(w=0, h=10, txt= '', border='', align='C', fill=False)
                        pdf_output = io.BytesIO()
                        pdf_output.write(pdf.output(dest='S').encode('latin1'))
                        pdf_output.seek(0)
                        response = HttpResponse(pdf_output.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'attachment; filename="Memorandum.pdf"'
                        actualizaImpresion(liquidacion,usuario)
                        return response
                except Exception as e:
                    error = str(e)
                    print(e)
                    return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
                finally:
                    connections['FEE'].close()
            else:
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
        elif codigo == 'R':
            user_has_permission = request.user.has_perm('Salary.I_Recibos')
            existe = ''
            if len(centros) == 0:
                centros = request.POST.get('Centro')
                existe = 'x'
                 
            #print(codigo,liquidacion,centros)
            if user_has_permission:
                recibos = Recibos()
                recibos.alias_nb_pages()
                recibos.add_page()

                if existe == 'x':
                    data = legajosOrdenadosUnico(lista,liquidacion,centros)
                else:
                    #print(lista,liquidacion,centros)
                    data = legajosOrdenados(lista,liquidacion,centros)

                cantidad = len(data)
                for item in data:
                    abrev = item['Abrev']
                    centro = item['Centro']
                    legajo = item['Legajo']
                    nombre = item['Nombre']
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt= 'LEGAJO: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt= str(legajo), border='', align='L', fill=False)
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt= 'APELLIDOS: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt= nombre, border='', align='L', fill=False)
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt= 'C. DE COSTO: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt= centro, border='', align='L', fill=False)
                    recibos.multi_cell(w=0, h=6, txt= '', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.cell(w=36, h=6, txt= 'CONCEPTO', border='', align='L', fill=False)
                    recibos.cell(w=36, h=6, txt= 'IMPORTE', border='', align='C', fill=False)
                    recibos.cell(w=26, h=6, txt= 'FECHA', border='', align='C', fill=False)
                    recibos.multi_cell(w=0, h=6, txt= 'DETALES', border='', align='L', fill=False)

                    datos = detallesRecibos(legajo,liquidacion,abrev)
                    for item in datos:
                        concepto = str(item['Descripcion'])
                        parcial = str(item['Importe'])
                        detalles = str(item['Detalle']).replace('\n',' ')
                        fecha = str(item['Fecha'])
                        importe_total_uno = str(item['Total'])
                        recibos.set_font('Arial', '', 8)
                        recibos.cell(w=36, h=6, txt= concepto, border='', align='L', fill=False)
                        recibos.cell(w=36, h=6, txt= parcial, border='', align='C', fill=False)
                        recibos.cell(w=26, h=6, txt= fecha, border='', align='C', fill=False)
                        recibos.multi_cell(w=0, h=6, txt= detalles, border='', align='L', fill=False)        
                    recibos.set_y(126) 
                    recibos.set_font('Arial', '', 10)
                    recibos.multi_cell(w=0, h=6, txt='TOTAL: ' + importe_total_uno, border='', align='R', fill=False)



                    recibos.set_y(148)
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt='LEGAJO: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt= str(legajo), border='', align='L', fill=False)
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt='APELLIDOS: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt= nombre, border='', align='L', fill=False)
                    recibos.set_font('Arial', '', 10)
                    recibos.cell(w=26, h=6, txt='C. DE COSTO: ', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.multi_cell(w=0, h=6, txt=centro, border='', align='L', fill=False)
                    recibos.multi_cell(w=0, h=6, txt='', border='', align='L', fill=False)
                    recibos.set_font('Arial', 'B', 10)
                    recibos.cell(w=36, h=6, txt= 'CONCEPTO', border='', align='L', fill=False)
                    recibos.cell(w=36, h=6, txt= 'IMPORTE', border='', align='C', fill=False)
                    recibos.cell(w=26, h=6, txt= 'FECHA', border='', align='C', fill=False)
                    recibos.multi_cell(w=0, h=6, txt= 'DETALES', border='', align='L', fill=False)
                    for item in datos:
                        concepto = str(item['Descripcion'])
                        parcial = str(item['Importe'])
                        detalles = str(item['Detalle']).replace('\n',' ')
                        fecha = str(item['Fecha'])
                        importe_total_dos = str(item['Total'])
                        recibos.set_font('Arial', '', 8)
                        recibos.cell(w=36, h=6, txt= concepto, border='', align='L', fill=False)
                        recibos.cell(w=36, h=6, txt= parcial, border='', align='C', fill=False)
                        recibos.cell(w=26, h=6, txt= fecha, border='', align='C', fill=False)
                        recibos.multi_cell(w=0, h=6, txt= detalles, border='', align='L', fill=False)

                    recibos.set_y(270) 
                    recibos.set_font('Arial', '', 10)
                    recibos.multi_cell(w=0, h=6, txt='TOTAL: ' + importe_total_dos, border='', align='R', fill=False)
                    cantidad = cantidad - 1
                    if cantidad != 0:
                        recibos.add_page()
                
                pdf_output = io.BytesIO()
                pdf_output.write(recibos.output(dest='S').encode('latin1'))
                pdf_output.seek(0)
                response = HttpResponse(pdf_output.read(), content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="Recibos.pdf"'
                return response
            else:
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
        elif codigo == 'P':
            user_has_permission = request.user.has_perm('Salary.I_Planillas')
            if user_has_permission:
                importeTotalPlanilla, nombreLiquidacionPlanilla = consultaImporteLuidacion(liquidacion,centros)

                planillas = PlanillasAdicionales(nombreLiquidacionPlanilla,importeTotalPlanilla)
                planillas.alias_nb_pages()
                planillas.add_page()
                try:
                    with connections['FEE'].cursor() as cursor:
                        sql3 = """ SELECT Abrev, Descripcion FROM S_CentrosCostos WHERE Abrev = %s """
                        for item in centros:
                            cursor.execute(sql3, (str(item),))
                            consultaPlanilla = cursor.fetchone()
                            if consultaPlanilla:
                                abrevPlanilla = consultaPlanilla[0]
                                centroNombrePlanilla = str(consultaPlanilla[1])
                            planillas.set_fill_color(186, 233, 175)
                            planillas.set_font('Arial', 'B', 14)
                            planillas.multi_cell(w=0, h=6, txt= centroNombrePlanilla, border='', align='l', fill=False)
                            planillas.set_font('Arial', 'B', 12)
                            planillas.cell(w=22, h=6, txt= 'LEGAJO', border='TLB', align='C', fill=True)
                            planillas.cell(w=100, h=6, txt= 'APELLIDOS Y NOMBRES', border='TLB', align='C', fill=True)
                            planillas.cell(w=24, h=6, txt= 'CANTIDAD', border='TLB', align='C', fill=True)
                            planillas.multi_cell(w=0, h=6, txt= 'IMPORTE', border='TLBR', align='C', fill=True)
                            sql = f"""
                                SELECT 
                                    A.IdLegajo AS LEGAJO, CONCAT(L.Apellidos, ' ', L.Nombres, ' (', L.AbrevCosto,')') AS NOMBRES, C.Descripcion AS CENTRO, COUNT(A.ID_A) AS CANTIDAD_ADICIONALES, SUM(A.Importe) AS TOTAL_IMPORTE
                                FROM 
                                    S_Adicionales A  INNER JOIN 
                                    S_Legajos L ON A.IdLegajo = L.IdLegajo  LEFT JOIN 
                                    S_CentrosCostos C ON L.AbrevCosto = C.Abrev
                                WHERE 
                                    A.IdLiquidacion = %s AND A.Abrev = %s AND A.Estado = 'L'
                                GROUP BY 
                                    A.IdLegajo, 
                                    L.Apellidos, 
                                    L.Nombres, 
                                    C.Descripcion,
                                    L.AbrevCosto
                                ORDER BY 
                                    L.Apellidos;
                                """
                            cursor.execute(sql, (liquidacion,item))
                            consulta = cursor.fetchall()
                            if consulta:
                                for row in consulta:
                                    legajoP = str(row[0])
                                    nombreP = str(row[1])
                                    centroP = str(row[2])
                                    cantidadP = str(row[3])
                                    importeP = formatear_numero(row[4])
                                    planillas.set_font('Arial', '', 10)
                                    planillas.cell(w=22, h=6, txt= legajoP, border='LBR', align='C', fill=False)
                                    planillas.cell(w=100, h=6, txt= nombreP, border='LB', align='L', fill=False)
                                    planillas.cell(w=24, h=6, txt= cantidadP, border='LB', align='C', fill=False)
                                    planillas.multi_cell(w=0, h=6, txt= importeP, border='LBR', align='C', fill=False)
                                planillas.multi_cell(w=0, h=10, txt= '', border='', align='', fill=False)

                        pdf_outputP = io.BytesIO()
                        pdf_outputP.write(planillas.output(dest='S').encode('latin1'))
                        pdf_outputP.seek(0)
                        response = HttpResponse(pdf_outputP.read(), content_type='application/pdf')
                        response['Content-Disposition'] = 'attachment; filename="Planillas.pdf"'
                        return response
                except Exception as e:
                    error = str(e)
                    return JsonResponse ({'Message': 'Not Found', 'Nota': 'Se produjo un error al intentar resolver la petición. ' + error})
                finally:
                    connections['FEE'].close()
            else:
                return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})   
    

def consultaImporteLuidacion(liquidacion,centros):
    centros_str = ', '.join([f"'{centro}'" for centro in centros])
    importeTotal = ''
    nombreLiquidacion = ''
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = f""" SELECT SUM(Importe), S.Carpeta
                        FROM S_Adicionales A INNER JOIN 
                            S_Legajos L ON A.IdLegajo = L.IdLegajo INNER JOIN 
                            S_Liquidaciones S ON A.IdLiquidacion = S.ID_L
                        WHERE IdLiquidacion = %s AND A.Abrev IN ({centros_str}) """
            cursor.execute(sql2, (liquidacion,))
            consultasql2 = cursor.fetchone()
            if consultasql2:
                importeTotal = formatear_numero(consultasql2[0])
                nombreLiquidacion = str(consultasql2[1])
        
            return importeTotal, nombreLiquidacion
    except Exception as e:
        error = str(e)
        return importeTotal, nombreLiquidacion
    finally:
        connections['FEE'].close()

def listaLegajos(liquidacion,centros):
    centros_str = ', '.join([f"'{centro}'" for centro in centros])
    listado = []
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = f"""SELECT DISTINCT A.IdLegajo 
                    FROM S_Adicionales A INNER JOIN
                        S_Legajos L ON A.IdLegajo = L.IdLegajo
                    WHERE A.IdLiquidacion = %s AND A.Abrev IN ({centros_str}) ; """
            cursor.execute(sql2, (liquidacion,))
            consultasql2 = cursor.fetchall()
            if consultasql2:
                for item in consultasql2:
                    legajo = str(item[0])
                    listado.append(legajo)
            return listado
    except Exception as e:
        error = str(e)
        return listado
    finally:
        connections['FEE'].close()

def listaLegajosNombreCentro(idLiquidacion,legajo):
    nombre_r = ''
    centro_r = ''
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """ SELECT 
                            CONCAT(L.Apellidos, ' ', L.Nombres, ' (', L.AbrevCosto,')') AS NOMBRE, 
                            CONCAT(C.Abrev, ' - ', C.Descripcion) AS CENTRO
                        FROM 
                            S_Legajos L 
                        LEFT JOIN 
                            S_CentrosCostos C 
                        ON 
                            C.Abrev = (
                                SELECT DISTINCT Abrev 
                                FROM S_Adicionales 
                                WHERE IdLegajo = L.IdLegajo AND IdLiquidacion = %s
                                LIMIT 1
                            )
                        WHERE 
                            L.IdLegajo = %s; """
            cursor.execute(sql2, (idLiquidacion,legajo))
            consulta = cursor.fetchone()
            if consulta:
                nombre_r = str(consulta[0])
                centro_r = str(consulta[1])
            return nombre_r, centro_r
    except Exception as e:
        error = str(e)
        return nombre_r, centro_r
    finally:
        connections['FEE'].close()

def actualizaImpresion(liquidacion,usuario):
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """ UPDATE S_Liquidaciones
                    SET Impresiones = Impresiones + 1,
                        UsuarioImpresiones = CONCAT(UsuarioImpresiones, ' - ', %s)
                    WHERE ID_L = %s; """
            cursor.execute(sql2, (usuario,liquidacion))
            
    except Exception as e:
        error = str(e)
    finally:
        connections['FEE'].close()

def detallesItems(legajo, liquidacion):
    total_sin = ''
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """  SELECT C.Descripcion, A.Importe, A.Detalle, DATE_FORMAT(Fecha, '%%d/%%m/%%Y'),
                        (SELECT SUM(Importe) FROM S_Adicionales WHERE IdLegajo = %s AND IdLiquidacion = %s) AS ImporteTotal
                        FROM S_Adicionales A 
                            INNER JOIN S_Conceptos C ON A.IdConcepto = C.ID_SC
                        WHERE IdLegajo = %s AND IdLiquidacion = %s; """
            cursor.execute(sql2, (legajo, liquidacion, legajo, liquidacion))
            consulta = cursor.fetchall()
            data = []
            total = 0
            if consulta:
                for row in consulta:
                    descripcion = str(row[0])
                    importe = formatear_numero(row[1])
                    detalle = str(row[2])
                    fecha = str(row[3])
                    total = formatear_numero(row[4])
                    total_sin = str(row[4])
                    data.append({
                        'descripcion': descripcion,
                        'importe': importe,
                        'fecha':fecha,
                        'detalle': detalle,
                        'total': total,
                        'total_sin': total_sin
                    })
                return json.dumps({'data': data, 'total_sin':total_sin})
    except Exception as e:
        error = str(e)
        print(error)

def detallesItems2(legajo, liquidacion, centro):
    total_sin = ''
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """ SELECT C.Descripcion, A.Importe, A.Detalle, DATE_FORMAT(Fecha, '%%d/%%m/%%Y'),
                        (SELECT SUM(Importe) FROM S_Adicionales WHERE IdLegajo = %s AND IdLiquidacion = %s AND Abrev = %s) AS ImporteTotal
                        FROM S_Adicionales A 
                            INNER JOIN S_Conceptos C ON A.IdConcepto = C.ID_SC
                        WHERE IdLegajo = %s AND IdLiquidacion = %s AND Abrev = %s; """
            cursor.execute(sql2, (legajo, liquidacion, centro, legajo, liquidacion,centro))
            consulta = cursor.fetchall()
            data = []
            total = 0
            if consulta:
                for row in consulta:
                    descripcion = str(row[0])
                    importe = formatear_numero(row[1])
                    detalle = str(row[2])
                    fecha = str(row[3])
                    total = formatear_numero(row[4])
                    total_sin = str(row[4])
                    data.append({
                        'descripcion': descripcion,
                        'importe': importe,
                        'fecha':fecha,
                        'detalle': detalle,
                        'total': total,
                        'total_sin': total_sin
                    })
                #print(json.dumps({'data': data, 'total_sin':total_sin}))
                return data
    except Exception as e:
        error = str(e)
        print("ERROORRRR" + error)

def detallesRecibos(legajo, liquidacion, centro):
    data = []
    total_sin = ''
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = """ SELECT C.Descripcion, A.Importe, A.Detalle, DATE_FORMAT(Fecha, '%%d/%%m/%%Y'),
                        (SELECT SUM(Importe) FROM S_Adicionales WHERE IdLegajo = %s AND IdLiquidacion = %s AND Abrev = %s) AS ImporteTotal
                        FROM S_Adicionales A 
                            INNER JOIN S_Conceptos C ON A.IdConcepto = C.ID_SC
                        WHERE IdLegajo = %s AND IdLiquidacion = %s AND Abrev = %s; """
            cursor.execute(sql2, (legajo, liquidacion, centro, legajo, liquidacion,centro))
            consulta = cursor.fetchall()
            total = 0
            if consulta:
                for row in consulta:
                    descripcion = str(row[0])
                    importe = formatear_numero(row[1])
                    detalle = str(row[2])
                    fecha = str(row[3])
                    total = formatear_numero(row[4])
                    total_sin = str(row[4])
                    datos = {'Descripcion': descripcion, 'Importe':importe, 'Fecha':fecha, 'Detalle': detalle, 'Total': total, 'TotalSin': total_sin}
                    data.append(datos)
                return data
    except Exception as e:
        error = str(e)
        print(error)
        return data

def detallesItemsConCentro(centro, liquidacion, lista):
    lista_str = ', '#.join([f"'{c}'" for c in lista])
    try:
        with connections['FEE'].cursor() as cursor:
            billetes_acumulados = {}
            for legajo in lista:
                sql2 = """ SELECT SUM(A.Importe)
                            FROM S_Adicionales A 
                                INNER JOIN S_Conceptos C ON A.IdConcepto = C.ID_SC
                            WHERE A.Abrev = %s AND IdLiquidacion = %s AND A.IdLegajo = %s; """
                cursor.execute(sql2, (centro, liquidacion, legajo))
                consulta = cursor.fetchone()
                if consulta and consulta[0]:
                    importe = float(consulta[0])
                    datas = calcular_billetes_legajo(importe)
                    billetes = datas["billetes"]
                    for denominacion, datos in billetes.items():
                        if denominacion not in billetes_acumulados:
                            billetes_acumulados[denominacion] = {
                                "cantidad": 0,
                                "importe_parcial": 0
                            }
                        billetes_acumulados[denominacion]["cantidad"] += datos["cantidad"]
                        billetes_acumulados[denominacion]["importe_parcial"] += datos["importe_parcial"]

            billetes_acumulados_ordenados = OrderedDict(
                sorted(billetes_acumulados.items(), key=lambda x: x[0], reverse=True)
            )

            billetes_acumulados_json = json.dumps(billetes_acumulados_ordenados, indent=4)
            return json.dumps({'billetes_acumulados': billetes_acumulados_ordenados})
    except Exception as e:
        error = str(e)
        print(error)

def ordenRecibos(legajos):
    legajos_str = ', '.join([f"'{legajo}'" for legajo in legajos])
    listado = []
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = f""" 
                    SELECT IdLegajo, CONCAT(Apellidos, ' ', Nombres, ' (', AbrevCosto, ')') AS NOMBRES
                    FROM S_Legajos 
                    WHERE IdLegajo IN ({legajos_str})
                    ORDER BY CONCAT(Apellidos, ' ', Nombres);
                 """
            cursor.execute(sql2)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    legajo = str(i[0])
                    listado.append(legajo)
                return listado
            else:
                return listado
    except Exception as e:
        error = str(e)
        return listado
    finally:
        connections['FEE'].close()


def legajosOrdenados(legajos,liquidacion, centro):
    legajos_str = ', '.join([f"'{legajo}'" for legajo in legajos])
    centros_str = ', '.join([f"'{c}'" for c in centro])
    listado = []
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = f""" 
                    SELECT DISTINCT 
                        A.Abrev,
                        CONCAT(C.Descripcion, ' - (',A.Abrev,')'),
                        L.IdLegajo, 
                        CONCAT(L.Apellidos, ' ', L.Nombres, ' (', L.AbrevCosto, ')') AS NOMBRES
                    FROM 
                        S_Legajos L 
                    INNER JOIN 
                        S_Adicionales A ON L.IdLegajo = A.IdLegajo
                    INNER JOIN	
                        S_CentrosCostos C ON A.Abrev = C.Abrev
                    WHERE 
                        L.IdLegajo IN ({legajos_str})
                        AND A.IdLiquidacion = '{liquidacion}'
                        AND A.Abrev IN ({centros_str})
                    ORDER BY 
                        NOMBRES;
                 """
            cursor.execute(sql2)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    abrev = str(i[0])
                    centro = str(i[1])
                    legajo = str(i[2])
                    nombre = str(i[3])
                    datos = {'Abrev': abrev, 'Centro': centro, 'Legajo': legajo, 'Nombre': nombre}
                    listado.append(datos)
                #print(listado)
                return listado
            else:
                return listado
    except Exception as e:
        error = str(e)
        return listado
    finally:
        connections['FEE'].close()

def legajosOrdenadosUnico(legajos,liquidacion,centro):
    legajos_str = ', '.join([f"'{legajo}'" for legajo in legajos])
    listado = []
    try:
        with connections['FEE'].cursor() as cursor:
            sql2 = f""" 
                    SELECT DISTINCT 
                        A.Abrev,
                        CONCAT(C.Descripcion, ' - (',A.Abrev,')'),
                        L.IdLegajo, 
                        CONCAT(L.Apellidos, ' ', L.Nombres, ' (', L.AbrevCosto, ')') AS NOMBRES
                    FROM 
                        S_Legajos L 
                    INNER JOIN 
                        S_Adicionales A ON L.IdLegajo = A.IdLegajo
                    INNER JOIN	
                        S_CentrosCostos C ON A.Abrev = C.Abrev
                    WHERE 
                        L.IdLegajo IN ({legajos_str})
                        AND A.Abrev = ('{centro}')
                        AND A.IdLiquidacion = '{liquidacion}'
                    ORDER BY 
                        NOMBRES;
                 """
            cursor.execute(sql2)
            consulta = cursor.fetchall()
            if consulta:
                for i in consulta:
                    abrev = str(i[0])
                    centro = str(i[1])
                    legajo = str(i[2])
                    nombre = str(i[3])
                    datos = {'Abrev': abrev, 'Centro': centro, 'Legajo': legajo, 'Nombre': nombre}
                    listado.append(datos)
                #print(listado)
                return listado
            else:
                return listado
    except Exception as e:
        error = str(e)
        return listado
    finally:
        connections['FEE'].close()

# def ordenRecibosnew(centros):
#     legajos_str = ', '.join([f"'{legajo}'" for legajo in legajos])
#     listado = []
#     try:
#         with connections['FEE'].cursor() as cursor:
#             sql2 = f""" 
#                     SELECT IdLegajo, CONCAT(Apellidos, ' ', Nombres, ' (', AbrevCosto, ')') AS NOMBRES
#                     FROM S_Legajos 
#                     WHERE IdLegajo IN ({legajos_str})
#                     ORDER BY CONCAT(Apellidos, ' ', Nombres);
#                  """
#             cursor.execute(sql2)
#             consulta = cursor.fetchall()
#             if consulta:
#                 for i in consulta:
#                     legajo = str(i[0])
#                     listado.append(legajo)
#                 return listado
#             else:
#                 return listado
#     except Exception as e:
#         error = str(e)
#         return listado
#     finally:
#         connections['FEE'].close()

class Memorandum(FPDF):
    def __init__(self, solicitante, liquidacion, importe):
        super().__init__()
        self.solicitante = solicitante
        self.liquidacion = liquidacion
        self.importe = importe


    def header(self):
        self.set_font('Arial', 'B', 14)
        self.text(x=84, y=11, txt= 'MEMORANDUM')
        self.line(10,13,200,13)
        self.set_font('Arial', '', 8)
        self.text(x=152, y=10, txt= fechaString())
        self.set_font('Arial', '', 10)
        self.text(x=150, y=18, txt= 'CIPOLLETI - R.N.')
        self.text(x=150, y=23, txt= 'ADMINISTRACIÓN')
        self.text(x=12, y=18, txt= 'LIQUIDACIÓN: ')
        self.text(x=12, y=23, txt= 'SOLICITA: ')
        self.text(x=12, y=28, txt= 'SOLICITA EL IMPORTE DE: ')
        self.set_font('Arial', 'B', 10)
        self.text(x=60, y=18, txt= self.liquidacion)
        self.text(x=60, y=23, txt= 'TORRES PATRICIO ALEJANDRO')
        self.text(x=60, y=28, txt= self.importe)
        self.rect(x=10,y=6,w=190,h=24)
        self.ln(26)

    def footer(self):
        self.set_font('Arial', '', 10)
        self.set_y(-18)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')
        self.text(x=40, y=292, txt= 'Solicita')
        self.text(x=120, y=292, txt= 'Autoriza')
        self.set_font('Arial', 'b', 8)
        self.text(x=30, y=288, txt= '.........................................')
        self.text(x=110, y=288, txt= '.........................................')

class PlanillasAdicionales(FPDF):

    def __init__(self, liquidacion, importe):
        super().__init__()
        self.liquidacion = liquidacion
        self.importe = importe

    def header(self):
        self.set_font('Arial', 'B', 14)
        self.text(x=52, y=11, txt= 'PLANILLAS DE ADICIONALES')
        self.line(10,13,200,13)
        self.set_font('Arial', '', 8)
        self.text(x=152, y=10, txt= fechaString())
        self.set_font('Arial', '', 10)
        self.text(x=150, y=18, txt= 'CIPOLLETI R.N.')
        self.text(x=150, y=23, txt= 'ADMINISTRACIÓN')
        self.text(x=12, y=18, txt= 'LIQUIDACIÓN: ')
        self.text(x=12, y=23, txt= 'IMPORTE TOTAL: ')
        self.set_font('Arial', 'B', 10)
        self.text(x=60, y=18, txt= self.liquidacion)
        self.text(x=60, y=23, txt= self.importe)
        self.rect(x=10,y=6,w=190,h=20)
        self.ln(24)

    def footer(self):
        self.set_font('Arial', '', 10)
        self.set_y(-18)
        self.cell(0, 10, 'Página ' + str(self.page_no()) + '/{nb}', 0, 0, 'R')

class Recibos(FPDF):
    def header(self):
        self.ln(0)





# for centro in centros:
#     legajos_ordenados = ordenRecibos(lista)
#     for legajo_r in legajos_ordenados:
#         nombre_r, centro_r = listaLegajosNombreCentro(liquidacion,legajo_r)
#         recibos.set_font('Arial', '', 10)
#         recibos.cell(w=26, h=6, txt= 'LEGAJO: ', border='', align='L', fill=False)
#         recibos.set_font('Arial', 'B', 10)
#         recibos.multi_cell(w=0, h=6, txt= str(legajo_r), border='', align='L', fill=False)
#         recibos.set_font('Arial', '', 10)
#         recibos.cell(w=26, h=6, txt= 'APELLIDOS: ', border='', align='L', fill=False)
#         recibos.set_font('Arial', 'B', 10)
#         recibos.multi_cell(w=0, h=6, txt= nombre_r, border='', align='L', fill=False)
#         recibos.set_font('Arial', '', 10)
#         recibos.cell(w=26, h=6, txt= 'C. DE COSTO: ', border='', align='L', fill=False)
#         recibos.set_font('Arial', 'B', 10)
#         recibos.multi_cell(w=0, h=6, txt= centro_r, border='', align='L', fill=False)
#         recibos.multi_cell(w=0, h=6, txt= '', border='', align='L', fill=False)
#         recibos.set_font('Arial', 'B', 10)
#         recibos.cell(w=36, h=6, txt= 'CONCEPTO', border='', align='L', fill=False)
#         recibos.cell(w=36, h=6, txt= 'IMPORTE', border='', align='C', fill=False)
#         recibos.cell(w=26, h=6, txt= 'FECHA', border='', align='C', fill=False)
#         recibos.multi_cell(w=0, h=6, txt= 'DETALES', border='', align='L', fill=False)
        
#         datos = detallesItems2(legajo_r,liquidacion,centro)
#         datos_json = json.loads(datos)
#         for item in datos_json['data']:
#             concepto = str(item['descripcion'])
#             parcial = str(item['importe'])
#             detalles = str(item['detalle']).replace('\n',' ')
#             fecha = str(item['fecha'])
#             importe_total_uno = str(item['total'])
#             recibos.set_font('Arial', '', 8)
#             recibos.cell(w=36, h=6, txt= concepto, border='', align='L', fill=False)
#             recibos.cell(w=36, h=6, txt= parcial, border='', align='C', fill=False)
#             recibos.cell(w=26, h=6, txt= fecha, border='', align='C', fill=False)
#             recibos.multi_cell(w=0, h=6, txt= detalles, border='', align='L', fill=False)

        # recibos.set_y(126) 
        # recibos.set_font('Arial', '', 10)
        # recibos.multi_cell(w=0, h=6, txt='TOTAL: ' + importe_total_uno, border='', align='R', fill=False)
        # recibos.set_y(148)
        # recibos.set_font('Arial', '', 10)
        # recibos.cell(w=26, h=6, txt='LEGAJO: ', border='', align='L', fill=False)
        # recibos.set_font('Arial', 'B', 10)
        # recibos.multi_cell(w=0, h=6, txt= str(legajo_r), border='', align='L', fill=False)
        # recibos.set_font('Arial', '', 10)
        # recibos.cell(w=26, h=6, txt='APELLIDOS: ', border='', align='L', fill=False)
        # recibos.set_font('Arial', 'B', 10)
        # recibos.multi_cell(w=0, h=6, txt= nombre_r, border='', align='L', fill=False)
        # recibos.set_font('Arial', '', 10)
        # recibos.cell(w=26, h=6, txt='C. DE COSTO: ', border='', align='L', fill=False)
        # recibos.set_font('Arial', 'B', 10)
        # recibos.multi_cell(w=0, h=6, txt=centro_r, border='', align='L', fill=False)
        # recibos.multi_cell(w=0, h=6, txt='', border='', align='L', fill=False)
        # recibos.set_font('Arial', 'B', 10)
        # recibos.cell(w=36, h=6, txt= 'CONCEPTO', border='', align='L', fill=False)
        # recibos.cell(w=36, h=6, txt= 'IMPORTE', border='', align='C', fill=False)
        # recibos.cell(w=26, h=6, txt= 'FECHA', border='', align='C', fill=False)
        # recibos.multi_cell(w=0, h=6, txt= 'DETALES', border='', align='L', fill=False)

#         for item in datos_json['data']:
#             concepto = str(item['descripcion'])
#             parcial = str(item['importe'])
#             detalles = str(item['detalle']).replace('\n',' ')
#             fecha = str(item['fecha'])
#             importe_total_dos = str(item['total'])
#             recibos.set_font('Arial', '', 8)
#             recibos.cell(w=36, h=6, txt= concepto, border='', align='L', fill=False)
#             recibos.cell(w=36, h=6, txt= parcial, border='', align='C', fill=False)
#             recibos.cell(w=26, h=6, txt= fecha, border='', align='C', fill=False)
#             recibos.multi_cell(w=0, h=6, txt= detalles, border='', align='L', fill=False)

#         recibos.set_y(270) 
#         recibos.set_font('Arial', '', 10)
#         recibos.multi_cell(w=0, h=6, txt='TOTAL: ' + importe_total_dos, border='', align='R', fill=False)
















    ### MODELOS PDF ###































