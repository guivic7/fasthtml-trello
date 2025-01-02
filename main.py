from fasthtml.common import *


app, rt, (columns, Column), (items, Item) = fast_app(
    "data/board.db",
    hdrs=(
        Link(
            rel="stylesheet",
            href="https://cdn.jsdelivr.net/npm/@mdi/font@7.4.47/css/materialdesignicons.min.css",
            type="text/css",
        ),
        Link(rel="stylesheet", href="assets/styles.css", type="text/css"),
    ),
    columns=dict(id=int, title=str, position=int, pk="id"),
    items=dict(id=int, content=str, column=int, position=int, pk="id"),
)


@patch
def __ft__(self: Column):
    items_list = Ul(
        *items(order_by="position", where=f"column={self.id}"),
        insert_form_toggle(
            self.id,
        ),
        cls="cards",
    )
    return Li(
        Div(H2(self.title), items_list),
    )


@patch
def __ft__(self: Item):
    return Li(
        P(self.content), A(Span(cls="mdi mdi-pencil-outline")), cls="card-container"
    )


@rt
def insert_form_toggle(column_id: int):
    return Li(
        A(
            Span(cls="mdi mdi-plus"),
            f"Add a {'list' if column_id == 0 else 'card'}",
            hx_post=insert_form,
            hx_vals={"column_id": column_id},
            hx_swap="outerHTML",
            cls="insert-toggle",
        ),
        id=("insert-column" if column_id == 0 else f"insert-column-{column_id}"),
        cls="" if column_id == 0 else "insert-item",
    )


@rt
def insert_form(column_id: int):
    return Form(
        Textarea(
            placeholder=(
                "Enter list name..." if column_id == 0 else "Enter a title..."
            ),
            id="title" if column_id == 0 else "content",
        ),
        Div(
            Button(
                "Add list" if column_id == 0 else "Add card",
                hx_post="/column/" if column_id == 0 else f"/item/",
                hx_vals={"column_id": column_id},
                target_id=(
                    "insert-column" if column_id == 0 else f"insert-column-{column_id}"
                ),
                hx_swap="beforebegin",
            ),
            A(
                Span(cls="mdi mdi-close"),
                id="insert-form-cancel",
                hx_post=insert_form_toggle,
                hx_vals={"column_id": column_id},
                target_id=(
                    "insert-column" if column_id == 0 else f"insert-column-{column_id}"
                ),
                hx_swap="outerHTML",
            ),
            cls="insert-controls",
        ),
    )


@rt("/")
def get():
    columns_list = Ul(*columns(order_by="position"), insert_form_toggle(0), id="lists")
    return Titled("FastHTML Trello Clone", columns_list, id="board")


@rt("/column/")
def post(column: Column):
    column.position = len(columns()) + 1
    return columns.insert(column)


@rt("/item/")
def post(item: Item, column_id: int):
    print(item)
    item.position = len(items()) + 1
    item.column = column_id
    return items.insert(item)


serve()
