from datasette import hookimpl


SCRIPT = """
(() => {
  const style = document.createElement("style");
  style.textContent = `
    .select-wrapper.column-select-wrapper {
      width: 22rem;
      max-width: 100%;
      height: 35px;
      overflow: visible;
      vertical-align: top;
    }

    .select-wrapper.column-select-wrapper::after {
      display: none;
    }

    .column-select-wrapper select.column-select-enhanced {
      display: none;
    }

    form.filters input.column-select-search[type="search"] {
      box-sizing: border-box;
      width: 100%;
      border: none;
      border-radius: 3px;
      font: inherit;
      height: 33px;
      padding: 8px 8px;
    }

    form.filters input.column-select-search[type="search"]:focus {
      outline: none;
    }

    .column-select-menu {
      position: absolute;
      top: calc(100% + 2px);
      left: 0;
      z-index: 20;
      box-sizing: border-box;
      min-width: 100%;
      width: max-content;
      max-width: min(42rem, calc(100vw - 2rem));
      max-height: 14rem;
      overflow-y: auto;
      background: #fff;
      border: 1px solid #ccc;
      border-radius: 3px;
      box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
    }

    .column-select-menu[hidden] {
      display: none;
    }

    .column-select-option {
      display: block;
      width: 100%;
      border: none;
      background: #fff;
      color: #222;
      cursor: pointer;
      font: inherit;
      line-height: 1.3;
      padding: 4px 8px;
      text-align: left;
      white-space: nowrap;
      -webkit-appearance: none;
      appearance: none;
    }

    .column-select-option:hover,
    .column-select-option:focus,
    .column-select-option.is-active {
      background: #f5f5f5;
    }
  `;
  document.head.appendChild(style);

  const sortSelect = (select) => {
    const selectedValue = select.value;
    const options = Array.from(select.options);
    const fixed = options.filter((option) => option.value === "");
    const sortable = options.filter((option) => option.value !== "");

    sortable.sort((a, b) =>
      a.text.localeCompare(b.text, undefined, {
        numeric: true,
        sensitivity: "base"
      })
    );

    select.replaceChildren(...fixed, ...sortable);
    if (Array.from(select.options).some((option) => option.value === selectedValue)) {
      select.value = selectedValue;
    }
  };

  const addSearchInput = (select, index) => {
    const options = Array.from(select.options).filter(
      (option) => option.value !== ""
    );

    const input = document.createElement("input");
    input.type = "search";
    input.className = "column-select-search";
    input.setAttribute("placeholder", "Search columns...");
    input.setAttribute("aria-label", "Search filter columns");
    input.value = select.value;

    const menu = document.createElement("div");
    menu.className = "column-select-menu";
    menu.id = `column-select-menu-${index}`;
    menu.hidden = true;
    input.setAttribute("aria-controls", menu.id);
    input.setAttribute("aria-expanded", "false");
    input.setAttribute("autocomplete", "off");

    let activeIndex = -1;

    const chooseOption = (option) => {
      select.value = option.value;
      input.value = option.text;
      hideMenu();
    };

    const hideMenu = () => {
      menu.hidden = true;
      input.setAttribute("aria-expanded", "false");
      activeIndex = -1;
    };

    const renderMenu = () => {
      const query = input.value.trim().toLowerCase();
      const matches = options.filter((option) =>
        option.text.toLowerCase().includes(query)
      );

      menu.replaceChildren();
      matches.forEach((option, optionIndex) => {
        const item = document.createElement("div");
        item.className = "column-select-option";
        item.setAttribute("role", "option");
        item.setAttribute("tabindex", "-1");
        item.textContent = option.text;
        item.addEventListener("mousedown", (event) => {
          event.preventDefault();
          chooseOption(option);
        });
        if (optionIndex === activeIndex) {
          item.classList.add("is-active");
        }
        menu.appendChild(item);
      });

      menu.hidden = matches.length === 0;
      input.setAttribute("aria-expanded", String(matches.length > 0));
    };

    input.addEventListener("input", () => {
      const exactMatch = options.find(
        (option) => option.text.toLowerCase() === input.value.trim().toLowerCase()
      );
      if (exactMatch) {
        select.value = exactMatch.value;
      } else if (input.value === "") {
        select.value = "";
      }
      activeIndex = -1;
      renderMenu();
    });

    input.addEventListener("focus", renderMenu);
    input.addEventListener("blur", hideMenu);
    input.addEventListener("keydown", (event) => {
      const items = Array.from(menu.querySelectorAll(".column-select-option"));
      if (event.key === "Escape") {
        hideMenu();
      } else if (event.key === "ArrowDown" && items.length) {
        event.preventDefault();
        activeIndex = (activeIndex + 1) % items.length;
        renderMenu();
      } else if (event.key === "ArrowUp" && items.length) {
        event.preventDefault();
        activeIndex = (activeIndex - 1 + items.length) % items.length;
        renderMenu();
      } else if (event.key === "Enter" && activeIndex >= 0 && items[activeIndex]) {
        event.preventDefault();
        items[activeIndex].dispatchEvent(new MouseEvent("mousedown"));
      }
    });

    select.classList.add("column-select-enhanced");
    select.parentNode.classList.add("column-select-wrapper");
    select.parentNode.insertBefore(input, select);
    select.parentNode.insertBefore(menu, select);
  };

  document
    .querySelectorAll('select[name^="_filter_column"]')
    .forEach((select, index) => {
      sortSelect(select);
      addSearchInput(select, index);
    });
})();
"""


@hookimpl
def extra_body_script(view_name):
    if view_name != "table":
        return None
    return SCRIPT
