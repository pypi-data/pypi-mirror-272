from typing import Type, Any

from sqladmin_integration.forms import get_model_form
from starlette.requests import Request
from wtforms import Form

from sqladmin import ModelView


class TranslatableModelView(ModelView):

    async def scaffold_form(self) -> Type[Form]:
        if self.form is not None:
            return self.form
        return await get_model_form(
            model=self.model,
            session_maker=self.session_maker,
            only=self._form_prop_names ,
            column_labels=self._column_labels,
            form_args=self.form_args,
            form_widget_args=self.form_widget_args,
            form_class=self.form_base_class,
            form_overrides=self.form_overrides,
            form_ajax_refs=self._form_ajax_refs,
            form_include_pk=self.form_include_pk,
            form_converter=self.form_converter,
        )

    async def insert_model(self, request: Request, data: dict) -> Any:
        obj = await super().insert_model(request, data)
        await self.insert_translations(obj, data)
        return obj

    async def update_model(self, request: Request, pk: str, data: dict) -> Any:
        obj = await super().update_model(request, pk, data)
        await self.update_translations(obj, data)
        return obj

    async def insert_translations(self, obj: Any, data: dict) -> Any:
        async with self.session_maker(expire_on_commit=False) as session:
            for field in obj.translation_fields.keys():
                for locale in obj.locales._member_names_:
                    new_obj = obj.translation_model(object=obj, locale=locale)
                    setattr(new_obj, field, data.get(f"{field}_{locale}", ""))
                    session.add(new_obj)
            await session.commit()
            return obj

    async def update_translations(self, obj: Any, data: dict) -> Any:
        async with self.session_maker(expire_on_commit=False) as session:
            for translation in obj.translations:
                for field in obj.translation_fields.keys():
                    setattr(translation, field, data.get(f"{field}_{translation.locale}", ""))
                    session.add(translation)
            await session.commit()
            return obj
