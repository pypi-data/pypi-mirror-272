from typing import (
    Any,
    Dict,
    Optional,
    Sequence,
    Type,
)

from sqladmin.ajax import QueryAjaxModelLoader
from sqladmin.forms import ModelConverter, ModelConverterBase, WTFORMS_ATTRS
from sqlalchemy import inspect as sqlalchemy_inspect
from sqlalchemy.orm import sessionmaker
from wtforms import (
    Field,
    Form,
)
from wtforms.utils import unset_value

from mixins import TranslatableMixin


async def get_model_form(
    model: type,
    session_maker: sessionmaker,
    only: Optional[Sequence[str]] = None,
    exclude: Optional[Sequence[str]] = None,
    column_labels: Optional[Dict[str, str]] = None,
    form_args: Optional[Dict[str, Dict[str, Any]]] = None,
    form_widget_args: Optional[Dict[str, Dict[str, Any]]] = None,
    form_class: Type[Form] = Form,
    form_overrides: Optional[Dict[str, Type[Field]]] = None,
    form_ajax_refs: Optional[Dict[str, QueryAjaxModelLoader]] = None,
    form_include_pk: bool = False,
    form_converter: Type[ModelConverterBase] = ModelConverter,
) -> Type[Form]:
    type_name = model.__name__ + "Form"
    converter = form_converter()
    mapper = sqlalchemy_inspect(model)
    form_args = form_args or {}
    form_widget_args = form_widget_args or {}
    column_labels = column_labels or {}
    form_overrides = form_overrides or {}
    form_ajax_refs = form_ajax_refs or {}

    attributes = []
    names = only or mapper.attrs.keys()
    for name in names:
        if exclude and name in exclude:
            continue
        attributes.append((name, mapper.attrs[name]))

    if isinstance(model, TranslatableMixin):
        translation_mapper = sqlalchemy_inspect(model.translation_model)
        names = translation_mapper.attrs.keys()
        for name in names:
            if name not in model.translation_fields.keys():
                continue
            for locale in model.locales._member_names_:
                attributes.append((f"{name}_{locale}", mapper.attrs[name]))

    field_dict = {}
    for name, attr in attributes:
        field_args = form_args.get(name, {})
        field_args["name"] = name

        field_widget_args = form_widget_args.get(name, {})
        label = column_labels.get(name, None)
        override = form_overrides.get(name, None)
        field = await converter.convert(
            model=model,
            prop=attr,
            session_maker=session_maker,
            field_args=field_args,
            field_widget_args=field_widget_args,
            label=label,
            override=override,
            form_include_pk=form_include_pk,
            form_ajax_refs=form_ajax_refs,
        )
        if field is not None:
            field_dict_key = WTFORMS_ATTRS.get(name, name)
            field_dict[field_dict_key] = field
    field_dict["process"] = process
    return type(type_name, (form_class,), field_dict)


def process(self, formdata=None, obj=None, data=None, extra_filters=None, **kwargs):
    """Process default and input data with each field.

    :param formdata: Input data coming from the client, usually
        ``request.form`` or equivalent. Should provide a "multi
        dict" interface to get a list of values for a given key,
        such as what Werkzeug, Django, and WebOb provide.
    :param obj: Take existing data from attributes on this object
        matching form field attributes. Only used if ``formdata`` is
        not passed.
    :param data: Take existing data from keys in this dict matching
        form field attributes. ``obj`` takes precedence if it also
        has a matching attribute. Only used if ``formdata`` is not
        passed.
    :param extra_filters: A dict mapping field attribute names to
        lists of extra filter functions to run. Extra filters run
        after filters passed when creating the field. If the form
        has ``filter_<fieldname>``, it is the last extra filter.
    :param kwargs: Merged with ``data`` to allow passing existing
        data as parameters. Overwrites any duplicate keys in
        ``data``. Only used if ``formdata`` is not passed.
    """
    formdata = self.meta.wrap_formdata(self, formdata)

    if data is not None:
        kwargs = dict(data, **kwargs)

    filters = extra_filters.copy() if extra_filters is not None else {}

    for name, field in self._fields.items():
        field_extra_filters = filters.get(name, [])

        inline_filter = getattr(self, "filter_%s" % name, None)
        if inline_filter is not None:
            field_extra_filters.append(inline_filter)

        if obj is not None and hasattr(obj, name):
            data = getattr(obj, name)
        elif name in kwargs:
            data = kwargs[name]
        else:
            data = unset_value

        if obj is not None and isinstance(obj, TranslatableMixin):
            unpreffixed_name = name.split("_")[0]
            if unpreffixed_name in obj.translation_fields.keys():
                for locale in obj.locales._member_names_:
                    if locale == name.split("_")[-1].lower():
                        for translation in obj.translations:
                            if translation.locale == locale:
                                data = getattr(translation, unpreffixed_name, unset_value)
        field.process(formdata, data, extra_filters=field_extra_filters)
