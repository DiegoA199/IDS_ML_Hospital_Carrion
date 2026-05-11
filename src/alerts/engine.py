"""Generación de alertas a partir de predicciones o entradas manuales."""


def build_alert(prediction_label, probability=None, **kwargs):
    """
    Construye el diccionario de alerta con campos para persistencia y dashboard.

    Parameters
    ----------
    prediction_label
        Etiqueta predicha o tipo de amenaza.
    probability
        Confianza / probabilidad asociada si el modelo la expone.
    kwargs
        ``modelo_usado``, ``backend``, ``estado``, ``tipo_amenaza``, ``revisado_por``, etc.
    """
    label = str(prediction_label)
    if label.lower() in ["normal", "0"]:
        severity = "Baja"
        impact = "No se identifica amenaza en el registro evaluado."
        action = "Continuar monitoreo y registrar evento."
    else:
        severity = "Alta"
        impact = "Posible tráfico malicioso o comportamiento anómalo detectado."
        action = "Revisar origen/destino, aislar equipo sospechoso y validar con personal TI."
    out = {
        "amenaza": label,
        "tipo_amenaza": kwargs.get("tipo_amenaza") or label,
        "severidad": severity,
        "probabilidad": probability,
        "impacto": impact,
        "accion_recomendada": action,
        "modelo_usado": kwargs.get("modelo_usado"),
        "estado": kwargs.get("estado") or "nueva",
        "revisado_por": kwargs.get("revisado_por"),
        "backend": kwargs.get("backend"),
    }
    if kwargs.get("alert_uuid"):
        out["alert_uuid"] = kwargs["alert_uuid"]
    return out
