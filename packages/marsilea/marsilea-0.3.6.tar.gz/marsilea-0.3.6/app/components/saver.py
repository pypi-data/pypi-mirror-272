import io

import streamlit as st


def save_fig(fig, dpi, format):
    img = io.BytesIO()
    fig.savefig(img, dpi=dpi, format=format, bbox_inches="tight")
    return img


class ChartSaver:
    dpi: float
    format: str

    def __init__(self, figure):
        self.fig = figure
        with st.form("Export Options"):
            st.header("Save Figure")
            self.save_options()
            save = st.form_submit_button("Confirm")
        if save:
            if self.fig is None:
                st.error("Please render first.", icon="😿")
            else:
                st.download_button(
                    label="Download Image",
                    data=self.serialize(),
                    file_name=f"result.{self.format}",
                )

    def serialize(self):
        img = io.BytesIO()
        self.fig.savefig(img, dpi=self.dpi, format=self.format, bbox_inches="tight")
        return img

    def save_options(self):
        self.dpi = st.number_input(
            "DPI", min_value=90, value=90, max_value=600, step=10
        )
        self.format = st.selectbox(
            "Format",
            options=["png", "svg", "pdf", "jpeg"],
            format_func=lambda x: x.upper(),
        )
