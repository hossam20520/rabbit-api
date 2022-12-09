TEMPLATE = """
from database import SessionLocal, engine
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


{%- for elements in element -%}
models_{{ elements }}.Base.metadata.create_all(bind=engine) {{'\n'}}
{%- endfor -%}


{{'\n'}}
{{'\n'}}
{{'\n'}}

app = FastAPI(){{'\n'}}
{%- for elements in element -%}  
app.include_router({{elements}}_router, tags=["{{ elements.capitalize() }}"], prefix="/api/v1.0/{{ elements }}") {{'\n'}}
{%- endfor -%}



"""