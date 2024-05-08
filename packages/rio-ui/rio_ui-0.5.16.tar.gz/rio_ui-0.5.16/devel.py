import rio


def make_slider(
    *,
    is_sensitive: bool = True,
) -> rio.Component:
    def _on_value_change(value):
        print(f"Slider -> {value}")

    return rio.Slider(
        minimum=0,
        maximum=20,
        value=5,
        step=4,
        on_change=_on_value_change,
        is_sensitive=is_sensitive,
    )


class RootComponent(rio.Component):
    def build(self) -> rio.Component:
        return rio.Grid(
            [
                rio.Text(
                    "Foo",
                    height=1,
                ),
                make_slider(),
            ],
            [
                rio.Text(
                    "Foo",
                    height=2,
                ),
                make_slider(
                    is_sensitive=False,
                ),
            ],
            [
                rio.Text(
                    "Foo",
                    height=3,
                ),
                make_slider(),
            ],
            [
                rio.Text(
                    "Foo",
                    height=4,
                ),
                make_slider(),
            ],
            rio.ProgressBar(),
            rio.ProgressBar(0.3),
            rio.Button(
                "fooooo",
                icon="material/edit",
            ),
            rio.Rectangle(
                content=rio.Text("Rectangle"),
                fill=self.session.theme.primary_color,
                ripple=True,
                width=20,
                height=20,
            ),
            rio.Card(
                content=rio.Text("Card"),
                color="primary",
                on_press=lambda: None,
                width=20,
                height=20,
            ),
            rio.ListView(
                rio.SimpleListItem("Clickable", on_press=lambda: None),
                rio.SimpleListItem("Clickable", on_press=lambda: None),
                rio.SimpleListItem("Dead"),
                rio.SimpleListItem("Clickable", on_press=lambda: None),
            ),
            rio.SwitcherBar(
                values=["foo", "bar", "baz"],
                icons=["material/home", "material/face", "material/castle"],
                spacing=1,
                align_x=0.5,
            ),
            row_spacing=1,
            width=30,
            margin=5,
            align_x=0.5,
            align_y=0.5,
        )


app = rio.App(
    build=RootComponent,
)

app.run_in_browser()
