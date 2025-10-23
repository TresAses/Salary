from django.db import models

# Create your models here.
class General(models.Model):
    class Meta:
        permissions = [
            ("C_Ingresa", "Conceptos Ingresa"),
            ("C_Inserta", "Conceptos Inserta"),
            ("C_Modifica", "Conceptos Modifica"),
            ("C_Elimina", "Conceptos Elimina"),

            ("CC_Ingresa", "Centros Ingresa"),
            ("CC_Inserta", "Centros Inserta"),
            ("CC_Modifica", "Centros Modifica"),
            ("CC_Elimina", "Centros Elimina"),

            ("L_Ingresa", "Legajos Ingresa"),
            ("L_Inserta", "Legajos Inserta"),
            ("L_Modifica", "Legajos Modifica"),
            ("L_Elimina", "Legajos Elimina"),

            ("A_Ingresa", "Adicional Ingresa"),
            ("A_Inserta", "Adicional Inserta"),
            ("A_Modifica", "Adicional Modifica"),
            ("A_Elimina", "Adicional Elimina"),

            ("LQ_Ingresa", "Liquidacion Ingresa"),
            ("LQ_Inserta", "Liquidacion Inserta"),
            ("LQ_Modifica", "Liquidacion Modifica"),
            ("LQ_Elimina", "Liquidacion Elimina"),
            ("LQ_AbreLiqui", "Abre Liquidacion"),

            ("P_Ingresa", "Pagos Ingresa"),
            ("P_Inserta", "Pagos Inserta"),
            ("P_Modifica", "Pagos Modifica"),
            ("P_Elimina", "Pagos Elimina"),

            ("I_Recibos", "Imprime Recibos"),
            ("I_Planillas", "Imprime Planillas"),
            ("I_Memo", "Imprime Memo"),


        
        ]