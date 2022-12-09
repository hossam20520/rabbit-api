TEMPLATE = """
from database import SessionLocal, engine
from auth.login import router as login_router
from auth.register import router as register_router
import users.models as models
from fastapi import Depends, FastAPI, HTTPException ,  Request {{'\n'}}
{%- for elements in element -%}
import {{ elements }}.models as models_{{ elements }} {{'\n'}}
{%- endfor -%}
{%- for elements in element -%}
from {{elements}}.routes import router as {{elements}}_router {{'\n'}}
{%- endfor -%}

{{'\n'}}
{{'\n'}}
{{'\n'}}
{{'\n'}}

models.Base.metadata.create_all(bind=engine) {{'\n'}}
{%- for elements in element -%}
models_{{ elements }}.Base.metadata.create_all(bind=engine) {{'\n'}}
{%- endfor -%}


{{'\n'}}
{{'\n'}}
{{'\n'}}

app = FastAPI(){{'\n'}}
{{ '\n' }}
app.include_router(login_router, tags=["login"], prefix="/api/v1.0/login")
app.include_router(register_router, tags=["register"], prefix="/api/v1.0/register"){{ '\n' }}
{%- for elements in element -%}  
app.include_router({{elements}}_router, tags=["{{ elements.capitalize() }}"], prefix="/api/v1.0/{{ elements }}") {{'\n'}}
{%- endfor -%}


"""