const {
  SvelteComponent: Yt,
  assign: Gt,
  create_slot: Ot,
  detach: Rt,
  element: Ht,
  get_all_dirty_from_scope: Jt,
  get_slot_changes: Kt,
  get_spread_update: Qt,
  init: Ut,
  insert: Wt,
  safe_not_equal: xt,
  set_dynamic_element_data: Oe,
  set_style: j,
  toggle_class: O,
  transition_in: yt,
  transition_out: qt,
  update_slot_base: $t
} = window.__gradio__svelte__internal;
function el(n) {
  let e, t, l;
  const i = (
    /*#slots*/
    n[18].default
  ), s = Ot(
    i,
    n,
    /*$$scope*/
    n[17],
    null
  );
  let a = [
    { "data-testid": (
      /*test_id*/
      n[7]
    ) },
    { id: (
      /*elem_id*/
      n[2]
    ) },
    {
      class: t = "block " + /*elem_classes*/
      n[3].join(" ") + " svelte-nl1om8"
    }
  ], r = {};
  for (let o = 0; o < a.length; o += 1)
    r = Gt(r, a[o]);
  return {
    c() {
      e = Ht(
        /*tag*/
        n[14]
      ), s && s.c(), Oe(
        /*tag*/
        n[14]
      )(e, r), O(
        e,
        "hidden",
        /*visible*/
        n[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        n[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        n[5] === "focus"
      ), O(
        e,
        "border_contrast",
        /*border_mode*/
        n[5] === "contrast"
      ), O(e, "hide-container", !/*explicit_call*/
      n[8] && !/*container*/
      n[9]), j(
        e,
        "height",
        /*get_dimension*/
        n[15](
          /*height*/
          n[0]
        )
      ), j(e, "width", typeof /*width*/
      n[1] == "number" ? `calc(min(${/*width*/
      n[1]}px, 100%))` : (
        /*get_dimension*/
        n[15](
          /*width*/
          n[1]
        )
      )), j(
        e,
        "border-style",
        /*variant*/
        n[4]
      ), j(
        e,
        "overflow",
        /*allow_overflow*/
        n[11] ? "visible" : "hidden"
      ), j(
        e,
        "flex-grow",
        /*scale*/
        n[12]
      ), j(e, "min-width", `calc(min(${/*min_width*/
      n[13]}px, 100%))`), j(e, "border-width", "var(--block-border-width)");
    },
    m(o, f) {
      Wt(o, e, f), s && s.m(e, null), l = !0;
    },
    p(o, f) {
      s && s.p && (!l || f & /*$$scope*/
      131072) && $t(
        s,
        i,
        o,
        /*$$scope*/
        o[17],
        l ? Kt(
          i,
          /*$$scope*/
          o[17],
          f,
          null
        ) : Jt(
          /*$$scope*/
          o[17]
        ),
        null
      ), Oe(
        /*tag*/
        o[14]
      )(e, r = Qt(a, [
        (!l || f & /*test_id*/
        128) && { "data-testid": (
          /*test_id*/
          o[7]
        ) },
        (!l || f & /*elem_id*/
        4) && { id: (
          /*elem_id*/
          o[2]
        ) },
        (!l || f & /*elem_classes*/
        8 && t !== (t = "block " + /*elem_classes*/
        o[3].join(" ") + " svelte-nl1om8")) && { class: t }
      ])), O(
        e,
        "hidden",
        /*visible*/
        o[10] === !1
      ), O(
        e,
        "padded",
        /*padding*/
        o[6]
      ), O(
        e,
        "border_focus",
        /*border_mode*/
        o[5] === "focus"
      ), O(
        e,
        "border_contrast",
        /*border_mode*/
        o[5] === "contrast"
      ), O(e, "hide-container", !/*explicit_call*/
      o[8] && !/*container*/
      o[9]), f & /*height*/
      1 && j(
        e,
        "height",
        /*get_dimension*/
        o[15](
          /*height*/
          o[0]
        )
      ), f & /*width*/
      2 && j(e, "width", typeof /*width*/
      o[1] == "number" ? `calc(min(${/*width*/
      o[1]}px, 100%))` : (
        /*get_dimension*/
        o[15](
          /*width*/
          o[1]
        )
      )), f & /*variant*/
      16 && j(
        e,
        "border-style",
        /*variant*/
        o[4]
      ), f & /*allow_overflow*/
      2048 && j(
        e,
        "overflow",
        /*allow_overflow*/
        o[11] ? "visible" : "hidden"
      ), f & /*scale*/
      4096 && j(
        e,
        "flex-grow",
        /*scale*/
        o[12]
      ), f & /*min_width*/
      8192 && j(e, "min-width", `calc(min(${/*min_width*/
      o[13]}px, 100%))`);
    },
    i(o) {
      l || (yt(s, o), l = !0);
    },
    o(o) {
      qt(s, o), l = !1;
    },
    d(o) {
      o && Rt(e), s && s.d(o);
    }
  };
}
function tl(n) {
  let e, t = (
    /*tag*/
    n[14] && el(n)
  );
  return {
    c() {
      t && t.c();
    },
    m(l, i) {
      t && t.m(l, i), e = !0;
    },
    p(l, [i]) {
      /*tag*/
      l[14] && t.p(l, i);
    },
    i(l) {
      e || (yt(t, l), e = !0);
    },
    o(l) {
      qt(t, l), e = !1;
    },
    d(l) {
      t && t.d(l);
    }
  };
}
function ll(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { height: s = void 0 } = e, { width: a = void 0 } = e, { elem_id: r = "" } = e, { elem_classes: o = [] } = e, { variant: f = "solid" } = e, { border_mode: u = "base" } = e, { padding: _ = !0 } = e, { type: d = "normal" } = e, { test_id: c = void 0 } = e, { explicit_call: v = !1 } = e, { container: F = !0 } = e, { visible: y = !0 } = e, { allow_overflow: S = !0 } = e, { scale: b = null } = e, { min_width: m = 0 } = e, C = d === "fieldset" ? "fieldset" : "div";
  const M = (g) => {
    if (g !== void 0) {
      if (typeof g == "number")
        return g + "px";
      if (typeof g == "string")
        return g;
    }
  };
  return n.$$set = (g) => {
    "height" in g && t(0, s = g.height), "width" in g && t(1, a = g.width), "elem_id" in g && t(2, r = g.elem_id), "elem_classes" in g && t(3, o = g.elem_classes), "variant" in g && t(4, f = g.variant), "border_mode" in g && t(5, u = g.border_mode), "padding" in g && t(6, _ = g.padding), "type" in g && t(16, d = g.type), "test_id" in g && t(7, c = g.test_id), "explicit_call" in g && t(8, v = g.explicit_call), "container" in g && t(9, F = g.container), "visible" in g && t(10, y = g.visible), "allow_overflow" in g && t(11, S = g.allow_overflow), "scale" in g && t(12, b = g.scale), "min_width" in g && t(13, m = g.min_width), "$$scope" in g && t(17, i = g.$$scope);
  }, [
    s,
    a,
    r,
    o,
    f,
    u,
    _,
    c,
    v,
    F,
    y,
    S,
    b,
    m,
    C,
    M,
    d,
    i,
    l
  ];
}
class nl extends Yt {
  constructor(e) {
    super(), Ut(this, e, ll, tl, xt, {
      height: 0,
      width: 1,
      elem_id: 2,
      elem_classes: 3,
      variant: 4,
      border_mode: 5,
      padding: 6,
      type: 16,
      test_id: 7,
      explicit_call: 8,
      container: 9,
      visible: 10,
      allow_overflow: 11,
      scale: 12,
      min_width: 13
    });
  }
}
const {
  SvelteComponent: il,
  attr: sl,
  create_slot: fl,
  detach: ol,
  element: al,
  get_all_dirty_from_scope: rl,
  get_slot_changes: ul,
  init: _l,
  insert: cl,
  safe_not_equal: dl,
  transition_in: ml,
  transition_out: bl,
  update_slot_base: hl
} = window.__gradio__svelte__internal;
function gl(n) {
  let e, t;
  const l = (
    /*#slots*/
    n[1].default
  ), i = fl(
    l,
    n,
    /*$$scope*/
    n[0],
    null
  );
  return {
    c() {
      e = al("div"), i && i.c(), sl(e, "class", "svelte-1hnfib2");
    },
    m(s, a) {
      cl(s, e, a), i && i.m(e, null), t = !0;
    },
    p(s, [a]) {
      i && i.p && (!t || a & /*$$scope*/
      1) && hl(
        i,
        l,
        s,
        /*$$scope*/
        s[0],
        t ? ul(
          l,
          /*$$scope*/
          s[0],
          a,
          null
        ) : rl(
          /*$$scope*/
          s[0]
        ),
        null
      );
    },
    i(s) {
      t || (ml(i, s), t = !0);
    },
    o(s) {
      bl(i, s), t = !1;
    },
    d(s) {
      s && ol(e), i && i.d(s);
    }
  };
}
function wl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e;
  return n.$$set = (s) => {
    "$$scope" in s && t(0, i = s.$$scope);
  }, [i, l];
}
class kl extends il {
  constructor(e) {
    super(), _l(this, e, wl, gl, dl, {});
  }
}
const {
  SvelteComponent: pl,
  attr: Re,
  check_outros: vl,
  create_component: yl,
  create_slot: ql,
  destroy_component: Cl,
  detach: Ce,
  element: Fl,
  empty: Ll,
  get_all_dirty_from_scope: Sl,
  get_slot_changes: zl,
  group_outros: Ml,
  init: Vl,
  insert: Fe,
  mount_component: Nl,
  safe_not_equal: jl,
  set_data: Il,
  space: Zl,
  text: Bl,
  toggle_class: oe,
  transition_in: be,
  transition_out: Le,
  update_slot_base: Dl
} = window.__gradio__svelte__internal;
function He(n) {
  let e, t;
  return e = new kl({
    props: {
      $$slots: { default: [Al] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      yl(e.$$.fragment);
    },
    m(l, i) {
      Nl(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i & /*$$scope, info*/
      10 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (be(e.$$.fragment, l), t = !0);
    },
    o(l) {
      Le(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Cl(e, l);
    }
  };
}
function Al(n) {
  let e;
  return {
    c() {
      e = Bl(
        /*info*/
        n[1]
      );
    },
    m(t, l) {
      Fe(t, e, l);
    },
    p(t, l) {
      l & /*info*/
      2 && Il(
        e,
        /*info*/
        t[1]
      );
    },
    d(t) {
      t && Ce(e);
    }
  };
}
function El(n) {
  let e, t, l, i;
  const s = (
    /*#slots*/
    n[2].default
  ), a = ql(
    s,
    n,
    /*$$scope*/
    n[3],
    null
  );
  let r = (
    /*info*/
    n[1] && He(n)
  );
  return {
    c() {
      e = Fl("span"), a && a.c(), t = Zl(), r && r.c(), l = Ll(), Re(e, "data-testid", "block-info"), Re(e, "class", "svelte-22c38v"), oe(e, "sr-only", !/*show_label*/
      n[0]), oe(e, "hide", !/*show_label*/
      n[0]), oe(
        e,
        "has-info",
        /*info*/
        n[1] != null
      );
    },
    m(o, f) {
      Fe(o, e, f), a && a.m(e, null), Fe(o, t, f), r && r.m(o, f), Fe(o, l, f), i = !0;
    },
    p(o, [f]) {
      a && a.p && (!i || f & /*$$scope*/
      8) && Dl(
        a,
        s,
        o,
        /*$$scope*/
        o[3],
        i ? zl(
          s,
          /*$$scope*/
          o[3],
          f,
          null
        ) : Sl(
          /*$$scope*/
          o[3]
        ),
        null
      ), (!i || f & /*show_label*/
      1) && oe(e, "sr-only", !/*show_label*/
      o[0]), (!i || f & /*show_label*/
      1) && oe(e, "hide", !/*show_label*/
      o[0]), (!i || f & /*info*/
      2) && oe(
        e,
        "has-info",
        /*info*/
        o[1] != null
      ), /*info*/
      o[1] ? r ? (r.p(o, f), f & /*info*/
      2 && be(r, 1)) : (r = He(o), r.c(), be(r, 1), r.m(l.parentNode, l)) : r && (Ml(), Le(r, 1, 1, () => {
        r = null;
      }), vl());
    },
    i(o) {
      i || (be(a, o), be(r), i = !0);
    },
    o(o) {
      Le(a, o), Le(r), i = !1;
    },
    d(o) {
      o && (Ce(e), Ce(t), Ce(l)), a && a.d(o), r && r.d(o);
    }
  };
}
function Pl(n, e, t) {
  let { $$slots: l = {}, $$scope: i } = e, { show_label: s = !0 } = e, { info: a = void 0 } = e;
  return n.$$set = (r) => {
    "show_label" in r && t(0, s = r.show_label), "info" in r && t(1, a = r.info), "$$scope" in r && t(3, i = r.$$scope);
  }, [s, a, l, i];
}
class Tl extends pl {
  constructor(e) {
    super(), Vl(this, e, Pl, El, jl, { show_label: 0, info: 1 });
  }
}
const {
  SvelteComponent: Xl,
  append: Ze,
  attr: K,
  bubble: Yl,
  create_component: Gl,
  destroy_component: Ol,
  detach: Ct,
  element: Be,
  init: Rl,
  insert: Ft,
  listen: Hl,
  mount_component: Jl,
  safe_not_equal: Kl,
  set_data: Ql,
  set_style: ae,
  space: Ul,
  text: Wl,
  toggle_class: V,
  transition_in: xl,
  transition_out: $l
} = window.__gradio__svelte__internal;
function Je(n) {
  let e, t;
  return {
    c() {
      e = Be("span"), t = Wl(
        /*label*/
        n[1]
      ), K(e, "class", "svelte-1lrphxw");
    },
    m(l, i) {
      Ft(l, e, i), Ze(e, t);
    },
    p(l, i) {
      i & /*label*/
      2 && Ql(
        t,
        /*label*/
        l[1]
      );
    },
    d(l) {
      l && Ct(e);
    }
  };
}
function en(n) {
  let e, t, l, i, s, a, r, o = (
    /*show_label*/
    n[2] && Je(n)
  );
  return i = new /*Icon*/
  n[0]({}), {
    c() {
      e = Be("button"), o && o.c(), t = Ul(), l = Be("div"), Gl(i.$$.fragment), K(l, "class", "svelte-1lrphxw"), V(
        l,
        "small",
        /*size*/
        n[4] === "small"
      ), V(
        l,
        "large",
        /*size*/
        n[4] === "large"
      ), V(
        l,
        "medium",
        /*size*/
        n[4] === "medium"
      ), e.disabled = /*disabled*/
      n[7], K(
        e,
        "aria-label",
        /*label*/
        n[1]
      ), K(
        e,
        "aria-haspopup",
        /*hasPopup*/
        n[8]
      ), K(
        e,
        "title",
        /*label*/
        n[1]
      ), K(e, "class", "svelte-1lrphxw"), V(
        e,
        "pending",
        /*pending*/
        n[3]
      ), V(
        e,
        "padded",
        /*padded*/
        n[5]
      ), V(
        e,
        "highlight",
        /*highlight*/
        n[6]
      ), V(
        e,
        "transparent",
        /*transparent*/
        n[9]
      ), ae(e, "color", !/*disabled*/
      n[7] && /*_color*/
      n[12] ? (
        /*_color*/
        n[12]
      ) : "var(--block-label-text-color)"), ae(e, "--bg-color", /*disabled*/
      n[7] ? "auto" : (
        /*background*/
        n[10]
      )), ae(
        e,
        "margin-left",
        /*offset*/
        n[11] + "px"
      );
    },
    m(f, u) {
      Ft(f, e, u), o && o.m(e, null), Ze(e, t), Ze(e, l), Jl(i, l, null), s = !0, a || (r = Hl(
        e,
        "click",
        /*click_handler*/
        n[14]
      ), a = !0);
    },
    p(f, [u]) {
      /*show_label*/
      f[2] ? o ? o.p(f, u) : (o = Je(f), o.c(), o.m(e, t)) : o && (o.d(1), o = null), (!s || u & /*size*/
      16) && V(
        l,
        "small",
        /*size*/
        f[4] === "small"
      ), (!s || u & /*size*/
      16) && V(
        l,
        "large",
        /*size*/
        f[4] === "large"
      ), (!s || u & /*size*/
      16) && V(
        l,
        "medium",
        /*size*/
        f[4] === "medium"
      ), (!s || u & /*disabled*/
      128) && (e.disabled = /*disabled*/
      f[7]), (!s || u & /*label*/
      2) && K(
        e,
        "aria-label",
        /*label*/
        f[1]
      ), (!s || u & /*hasPopup*/
      256) && K(
        e,
        "aria-haspopup",
        /*hasPopup*/
        f[8]
      ), (!s || u & /*label*/
      2) && K(
        e,
        "title",
        /*label*/
        f[1]
      ), (!s || u & /*pending*/
      8) && V(
        e,
        "pending",
        /*pending*/
        f[3]
      ), (!s || u & /*padded*/
      32) && V(
        e,
        "padded",
        /*padded*/
        f[5]
      ), (!s || u & /*highlight*/
      64) && V(
        e,
        "highlight",
        /*highlight*/
        f[6]
      ), (!s || u & /*transparent*/
      512) && V(
        e,
        "transparent",
        /*transparent*/
        f[9]
      ), u & /*disabled, _color*/
      4224 && ae(e, "color", !/*disabled*/
      f[7] && /*_color*/
      f[12] ? (
        /*_color*/
        f[12]
      ) : "var(--block-label-text-color)"), u & /*disabled, background*/
      1152 && ae(e, "--bg-color", /*disabled*/
      f[7] ? "auto" : (
        /*background*/
        f[10]
      )), u & /*offset*/
      2048 && ae(
        e,
        "margin-left",
        /*offset*/
        f[11] + "px"
      );
    },
    i(f) {
      s || (xl(i.$$.fragment, f), s = !0);
    },
    o(f) {
      $l(i.$$.fragment, f), s = !1;
    },
    d(f) {
      f && Ct(e), o && o.d(), Ol(i), a = !1, r();
    }
  };
}
function tn(n, e, t) {
  let l, { Icon: i } = e, { label: s = "" } = e, { show_label: a = !1 } = e, { pending: r = !1 } = e, { size: o = "small" } = e, { padded: f = !0 } = e, { highlight: u = !1 } = e, { disabled: _ = !1 } = e, { hasPopup: d = !1 } = e, { color: c = "var(--block-label-text-color)" } = e, { transparent: v = !1 } = e, { background: F = "var(--background-fill-primary)" } = e, { offset: y = 0 } = e;
  function S(b) {
    Yl.call(this, n, b);
  }
  return n.$$set = (b) => {
    "Icon" in b && t(0, i = b.Icon), "label" in b && t(1, s = b.label), "show_label" in b && t(2, a = b.show_label), "pending" in b && t(3, r = b.pending), "size" in b && t(4, o = b.size), "padded" in b && t(5, f = b.padded), "highlight" in b && t(6, u = b.highlight), "disabled" in b && t(7, _ = b.disabled), "hasPopup" in b && t(8, d = b.hasPopup), "color" in b && t(13, c = b.color), "transparent" in b && t(9, v = b.transparent), "background" in b && t(10, F = b.background), "offset" in b && t(11, y = b.offset);
  }, n.$$.update = () => {
    n.$$.dirty & /*highlight, color*/
    8256 && t(12, l = u ? "var(--color-accent)" : c);
  }, [
    i,
    s,
    a,
    r,
    o,
    f,
    u,
    _,
    d,
    v,
    F,
    y,
    l,
    c,
    S
  ];
}
class ln extends Xl {
  constructor(e) {
    super(), Rl(this, e, tn, en, Kl, {
      Icon: 0,
      label: 1,
      show_label: 2,
      pending: 3,
      size: 4,
      padded: 5,
      highlight: 6,
      disabled: 7,
      hasPopup: 8,
      color: 13,
      transparent: 9,
      background: 10,
      offset: 11
    });
  }
}
const {
  SvelteComponent: nn,
  append: Ne,
  attr: E,
  detach: sn,
  init: fn,
  insert: on,
  noop: je,
  safe_not_equal: an,
  set_style: R,
  svg_element: ve
} = window.__gradio__svelte__internal;
function rn(n) {
  let e, t, l, i;
  return {
    c() {
      e = ve("svg"), t = ve("g"), l = ve("path"), i = ve("path"), E(l, "d", "M18,6L6.087,17.913"), R(l, "fill", "none"), R(l, "fill-rule", "nonzero"), R(l, "stroke-width", "2px"), E(t, "transform", "matrix(1.14096,-0.140958,-0.140958,1.14096,-0.0559523,0.0559523)"), E(i, "d", "M4.364,4.364L19.636,19.636"), R(i, "fill", "none"), R(i, "fill-rule", "nonzero"), R(i, "stroke-width", "2px"), E(e, "width", "100%"), E(e, "height", "100%"), E(e, "viewBox", "0 0 24 24"), E(e, "version", "1.1"), E(e, "xmlns", "http://www.w3.org/2000/svg"), E(e, "xmlns:xlink", "http://www.w3.org/1999/xlink"), E(e, "xml:space", "preserve"), E(e, "stroke", "currentColor"), R(e, "fill-rule", "evenodd"), R(e, "clip-rule", "evenodd"), R(e, "stroke-linecap", "round"), R(e, "stroke-linejoin", "round");
    },
    m(s, a) {
      on(s, e, a), Ne(e, t), Ne(t, l), Ne(e, i);
    },
    p: je,
    i: je,
    o: je,
    d(s) {
      s && sn(e);
    }
  };
}
class un extends nn {
  constructor(e) {
    super(), fn(this, e, null, rn, an, {});
  }
}
const _n = [
  { color: "red", primary: 600, secondary: 100 },
  { color: "green", primary: 600, secondary: 100 },
  { color: "blue", primary: 600, secondary: 100 },
  { color: "yellow", primary: 500, secondary: 100 },
  { color: "purple", primary: 600, secondary: 100 },
  { color: "teal", primary: 600, secondary: 100 },
  { color: "orange", primary: 600, secondary: 100 },
  { color: "cyan", primary: 600, secondary: 100 },
  { color: "lime", primary: 500, secondary: 100 },
  { color: "pink", primary: 600, secondary: 100 }
], Ke = {
  inherit: "inherit",
  current: "currentColor",
  transparent: "transparent",
  black: "#000",
  white: "#fff",
  slate: {
    50: "#f8fafc",
    100: "#f1f5f9",
    200: "#e2e8f0",
    300: "#cbd5e1",
    400: "#94a3b8",
    500: "#64748b",
    600: "#475569",
    700: "#334155",
    800: "#1e293b",
    900: "#0f172a",
    950: "#020617"
  },
  gray: {
    50: "#f9fafb",
    100: "#f3f4f6",
    200: "#e5e7eb",
    300: "#d1d5db",
    400: "#9ca3af",
    500: "#6b7280",
    600: "#4b5563",
    700: "#374151",
    800: "#1f2937",
    900: "#111827",
    950: "#030712"
  },
  zinc: {
    50: "#fafafa",
    100: "#f4f4f5",
    200: "#e4e4e7",
    300: "#d4d4d8",
    400: "#a1a1aa",
    500: "#71717a",
    600: "#52525b",
    700: "#3f3f46",
    800: "#27272a",
    900: "#18181b",
    950: "#09090b"
  },
  neutral: {
    50: "#fafafa",
    100: "#f5f5f5",
    200: "#e5e5e5",
    300: "#d4d4d4",
    400: "#a3a3a3",
    500: "#737373",
    600: "#525252",
    700: "#404040",
    800: "#262626",
    900: "#171717",
    950: "#0a0a0a"
  },
  stone: {
    50: "#fafaf9",
    100: "#f5f5f4",
    200: "#e7e5e4",
    300: "#d6d3d1",
    400: "#a8a29e",
    500: "#78716c",
    600: "#57534e",
    700: "#44403c",
    800: "#292524",
    900: "#1c1917",
    950: "#0c0a09"
  },
  red: {
    50: "#fef2f2",
    100: "#fee2e2",
    200: "#fecaca",
    300: "#fca5a5",
    400: "#f87171",
    500: "#ef4444",
    600: "#dc2626",
    700: "#b91c1c",
    800: "#991b1b",
    900: "#7f1d1d",
    950: "#450a0a"
  },
  orange: {
    50: "#fff7ed",
    100: "#ffedd5",
    200: "#fed7aa",
    300: "#fdba74",
    400: "#fb923c",
    500: "#f97316",
    600: "#ea580c",
    700: "#c2410c",
    800: "#9a3412",
    900: "#7c2d12",
    950: "#431407"
  },
  amber: {
    50: "#fffbeb",
    100: "#fef3c7",
    200: "#fde68a",
    300: "#fcd34d",
    400: "#fbbf24",
    500: "#f59e0b",
    600: "#d97706",
    700: "#b45309",
    800: "#92400e",
    900: "#78350f",
    950: "#451a03"
  },
  yellow: {
    50: "#fefce8",
    100: "#fef9c3",
    200: "#fef08a",
    300: "#fde047",
    400: "#facc15",
    500: "#eab308",
    600: "#ca8a04",
    700: "#a16207",
    800: "#854d0e",
    900: "#713f12",
    950: "#422006"
  },
  lime: {
    50: "#f7fee7",
    100: "#ecfccb",
    200: "#d9f99d",
    300: "#bef264",
    400: "#a3e635",
    500: "#84cc16",
    600: "#65a30d",
    700: "#4d7c0f",
    800: "#3f6212",
    900: "#365314",
    950: "#1a2e05"
  },
  green: {
    50: "#f0fdf4",
    100: "#dcfce7",
    200: "#bbf7d0",
    300: "#86efac",
    400: "#4ade80",
    500: "#22c55e",
    600: "#16a34a",
    700: "#15803d",
    800: "#166534",
    900: "#14532d",
    950: "#052e16"
  },
  emerald: {
    50: "#ecfdf5",
    100: "#d1fae5",
    200: "#a7f3d0",
    300: "#6ee7b7",
    400: "#34d399",
    500: "#10b981",
    600: "#059669",
    700: "#047857",
    800: "#065f46",
    900: "#064e3b",
    950: "#022c22"
  },
  teal: {
    50: "#f0fdfa",
    100: "#ccfbf1",
    200: "#99f6e4",
    300: "#5eead4",
    400: "#2dd4bf",
    500: "#14b8a6",
    600: "#0d9488",
    700: "#0f766e",
    800: "#115e59",
    900: "#134e4a",
    950: "#042f2e"
  },
  cyan: {
    50: "#ecfeff",
    100: "#cffafe",
    200: "#a5f3fc",
    300: "#67e8f9",
    400: "#22d3ee",
    500: "#06b6d4",
    600: "#0891b2",
    700: "#0e7490",
    800: "#155e75",
    900: "#164e63",
    950: "#083344"
  },
  sky: {
    50: "#f0f9ff",
    100: "#e0f2fe",
    200: "#bae6fd",
    300: "#7dd3fc",
    400: "#38bdf8",
    500: "#0ea5e9",
    600: "#0284c7",
    700: "#0369a1",
    800: "#075985",
    900: "#0c4a6e",
    950: "#082f49"
  },
  blue: {
    50: "#eff6ff",
    100: "#dbeafe",
    200: "#bfdbfe",
    300: "#93c5fd",
    400: "#60a5fa",
    500: "#3b82f6",
    600: "#2563eb",
    700: "#1d4ed8",
    800: "#1e40af",
    900: "#1e3a8a",
    950: "#172554"
  },
  indigo: {
    50: "#eef2ff",
    100: "#e0e7ff",
    200: "#c7d2fe",
    300: "#a5b4fc",
    400: "#818cf8",
    500: "#6366f1",
    600: "#4f46e5",
    700: "#4338ca",
    800: "#3730a3",
    900: "#312e81",
    950: "#1e1b4b"
  },
  violet: {
    50: "#f5f3ff",
    100: "#ede9fe",
    200: "#ddd6fe",
    300: "#c4b5fd",
    400: "#a78bfa",
    500: "#8b5cf6",
    600: "#7c3aed",
    700: "#6d28d9",
    800: "#5b21b6",
    900: "#4c1d95",
    950: "#2e1065"
  },
  purple: {
    50: "#faf5ff",
    100: "#f3e8ff",
    200: "#e9d5ff",
    300: "#d8b4fe",
    400: "#c084fc",
    500: "#a855f7",
    600: "#9333ea",
    700: "#7e22ce",
    800: "#6b21a8",
    900: "#581c87",
    950: "#3b0764"
  },
  fuchsia: {
    50: "#fdf4ff",
    100: "#fae8ff",
    200: "#f5d0fe",
    300: "#f0abfc",
    400: "#e879f9",
    500: "#d946ef",
    600: "#c026d3",
    700: "#a21caf",
    800: "#86198f",
    900: "#701a75",
    950: "#4a044e"
  },
  pink: {
    50: "#fdf2f8",
    100: "#fce7f3",
    200: "#fbcfe8",
    300: "#f9a8d4",
    400: "#f472b6",
    500: "#ec4899",
    600: "#db2777",
    700: "#be185d",
    800: "#9d174d",
    900: "#831843",
    950: "#500724"
  },
  rose: {
    50: "#fff1f2",
    100: "#ffe4e6",
    200: "#fecdd3",
    300: "#fda4af",
    400: "#fb7185",
    500: "#f43f5e",
    600: "#e11d48",
    700: "#be123c",
    800: "#9f1239",
    900: "#881337",
    950: "#4c0519"
  }
};
_n.reduce(
  (n, { color: e, primary: t, secondary: l }) => ({
    ...n,
    [e]: {
      primary: Ke[e][t],
      secondary: Ke[e][l]
    }
  }),
  {}
);
function ue(n) {
  let e = ["", "k", "M", "G", "T", "P", "E", "Z"], t = 0;
  for (; n > 1e3 && t < e.length - 1; )
    n /= 1e3, t++;
  let l = e[t];
  return (Number.isInteger(n) ? n : n.toFixed(1)) + l;
}
function Se() {
}
function cn(n, e) {
  return n != n ? e == e : n !== e || n && typeof n == "object" || typeof n == "function";
}
const Lt = typeof window < "u";
let Qe = Lt ? () => window.performance.now() : () => Date.now(), St = Lt ? (n) => requestAnimationFrame(n) : Se;
const ce = /* @__PURE__ */ new Set();
function zt(n) {
  ce.forEach((e) => {
    e.c(n) || (ce.delete(e), e.f());
  }), ce.size !== 0 && St(zt);
}
function dn(n) {
  let e;
  return ce.size === 0 && St(zt), {
    promise: new Promise((t) => {
      ce.add(e = { c: n, f: t });
    }),
    abort() {
      ce.delete(e);
    }
  };
}
const re = [];
function mn(n, e = Se) {
  let t;
  const l = /* @__PURE__ */ new Set();
  function i(r) {
    if (cn(n, r) && (n = r, t)) {
      const o = !re.length;
      for (const f of l)
        f[1](), re.push(f, n);
      if (o) {
        for (let f = 0; f < re.length; f += 2)
          re[f][0](re[f + 1]);
        re.length = 0;
      }
    }
  }
  function s(r) {
    i(r(n));
  }
  function a(r, o = Se) {
    const f = [r, o];
    return l.add(f), l.size === 1 && (t = e(i, s) || Se), r(n), () => {
      l.delete(f), l.size === 0 && t && (t(), t = null);
    };
  }
  return { set: i, update: s, subscribe: a };
}
function Ue(n) {
  return Object.prototype.toString.call(n) === "[object Date]";
}
function De(n, e, t, l) {
  if (typeof t == "number" || Ue(t)) {
    const i = l - t, s = (t - e) / (n.dt || 1 / 60), a = n.opts.stiffness * i, r = n.opts.damping * s, o = (a - r) * n.inv_mass, f = (s + o) * n.dt;
    return Math.abs(f) < n.opts.precision && Math.abs(i) < n.opts.precision ? l : (n.settled = !1, Ue(t) ? new Date(t.getTime() + f) : t + f);
  } else {
    if (Array.isArray(t))
      return t.map(
        (i, s) => De(n, e[s], t[s], l[s])
      );
    if (typeof t == "object") {
      const i = {};
      for (const s in t)
        i[s] = De(n, e[s], t[s], l[s]);
      return i;
    } else
      throw new Error(`Cannot spring ${typeof t} values`);
  }
}
function We(n, e = {}) {
  const t = mn(n), { stiffness: l = 0.15, damping: i = 0.8, precision: s = 0.01 } = e;
  let a, r, o, f = n, u = n, _ = 1, d = 0, c = !1;
  function v(y, S = {}) {
    u = y;
    const b = o = {};
    return n == null || S.hard || F.stiffness >= 1 && F.damping >= 1 ? (c = !0, a = Qe(), f = y, t.set(n = u), Promise.resolve()) : (S.soft && (d = 1 / ((S.soft === !0 ? 0.5 : +S.soft) * 60), _ = 0), r || (a = Qe(), c = !1, r = dn((m) => {
      if (c)
        return c = !1, r = null, !1;
      _ = Math.min(_ + d, 1);
      const C = {
        inv_mass: _,
        opts: F,
        settled: !0,
        dt: (m - a) * 60 / 1e3
      }, M = De(C, f, n, u);
      return a = m, f = n, t.set(n = M), C.settled && (r = null), !C.settled;
    })), new Promise((m) => {
      r.promise.then(() => {
        b === o && m();
      });
    }));
  }
  const F = {
    set: v,
    update: (y, S) => v(y(u, n), S),
    subscribe: t.subscribe,
    stiffness: l,
    damping: i,
    precision: s
  };
  return F;
}
const {
  SvelteComponent: bn,
  append: P,
  attr: q,
  component_subscribe: xe,
  detach: hn,
  element: gn,
  init: wn,
  insert: kn,
  noop: $e,
  safe_not_equal: pn,
  set_style: ye,
  svg_element: T,
  toggle_class: et
} = window.__gradio__svelte__internal, { onMount: vn } = window.__gradio__svelte__internal;
function yn(n) {
  let e, t, l, i, s, a, r, o, f, u, _, d;
  return {
    c() {
      e = gn("div"), t = T("svg"), l = T("g"), i = T("path"), s = T("path"), a = T("path"), r = T("path"), o = T("g"), f = T("path"), u = T("path"), _ = T("path"), d = T("path"), q(i, "d", "M255.926 0.754768L509.702 139.936V221.027L255.926 81.8465V0.754768Z"), q(i, "fill", "#FF7C00"), q(i, "fill-opacity", "0.4"), q(i, "class", "svelte-43sxxs"), q(s, "d", "M509.69 139.936L254.981 279.641V361.255L509.69 221.55V139.936Z"), q(s, "fill", "#FF7C00"), q(s, "class", "svelte-43sxxs"), q(a, "d", "M0.250138 139.937L254.981 279.641V361.255L0.250138 221.55V139.937Z"), q(a, "fill", "#FF7C00"), q(a, "fill-opacity", "0.4"), q(a, "class", "svelte-43sxxs"), q(r, "d", "M255.923 0.232622L0.236328 139.936V221.55L255.923 81.8469V0.232622Z"), q(r, "fill", "#FF7C00"), q(r, "class", "svelte-43sxxs"), ye(l, "transform", "translate(" + /*$top*/
      n[1][0] + "px, " + /*$top*/
      n[1][1] + "px)"), q(f, "d", "M255.926 141.5L509.702 280.681V361.773L255.926 222.592V141.5Z"), q(f, "fill", "#FF7C00"), q(f, "fill-opacity", "0.4"), q(f, "class", "svelte-43sxxs"), q(u, "d", "M509.69 280.679L254.981 420.384V501.998L509.69 362.293V280.679Z"), q(u, "fill", "#FF7C00"), q(u, "class", "svelte-43sxxs"), q(_, "d", "M0.250138 280.681L254.981 420.386V502L0.250138 362.295V280.681Z"), q(_, "fill", "#FF7C00"), q(_, "fill-opacity", "0.4"), q(_, "class", "svelte-43sxxs"), q(d, "d", "M255.923 140.977L0.236328 280.68V362.294L255.923 222.591V140.977Z"), q(d, "fill", "#FF7C00"), q(d, "class", "svelte-43sxxs"), ye(o, "transform", "translate(" + /*$bottom*/
      n[2][0] + "px, " + /*$bottom*/
      n[2][1] + "px)"), q(t, "viewBox", "-1200 -1200 3000 3000"), q(t, "fill", "none"), q(t, "xmlns", "http://www.w3.org/2000/svg"), q(t, "class", "svelte-43sxxs"), q(e, "class", "svelte-43sxxs"), et(
        e,
        "margin",
        /*margin*/
        n[0]
      );
    },
    m(c, v) {
      kn(c, e, v), P(e, t), P(t, l), P(l, i), P(l, s), P(l, a), P(l, r), P(t, o), P(o, f), P(o, u), P(o, _), P(o, d);
    },
    p(c, [v]) {
      v & /*$top*/
      2 && ye(l, "transform", "translate(" + /*$top*/
      c[1][0] + "px, " + /*$top*/
      c[1][1] + "px)"), v & /*$bottom*/
      4 && ye(o, "transform", "translate(" + /*$bottom*/
      c[2][0] + "px, " + /*$bottom*/
      c[2][1] + "px)"), v & /*margin*/
      1 && et(
        e,
        "margin",
        /*margin*/
        c[0]
      );
    },
    i: $e,
    o: $e,
    d(c) {
      c && hn(e);
    }
  };
}
function qn(n, e, t) {
  let l, i;
  var s = this && this.__awaiter || function(c, v, F, y) {
    function S(b) {
      return b instanceof F ? b : new F(function(m) {
        m(b);
      });
    }
    return new (F || (F = Promise))(function(b, m) {
      function C(z) {
        try {
          g(y.next(z));
        } catch (w) {
          m(w);
        }
      }
      function M(z) {
        try {
          g(y.throw(z));
        } catch (w) {
          m(w);
        }
      }
      function g(z) {
        z.done ? b(z.value) : S(z.value).then(C, M);
      }
      g((y = y.apply(c, v || [])).next());
    });
  };
  let { margin: a = !0 } = e;
  const r = We([0, 0]);
  xe(n, r, (c) => t(1, l = c));
  const o = We([0, 0]);
  xe(n, o, (c) => t(2, i = c));
  let f;
  function u() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 140]), o.set([-125, -140])]), yield Promise.all([r.set([-125, 140]), o.set([125, -140])]), yield Promise.all([r.set([-125, 0]), o.set([125, -0])]), yield Promise.all([r.set([125, 0]), o.set([-125, 0])]);
    });
  }
  function _() {
    return s(this, void 0, void 0, function* () {
      yield u(), f || _();
    });
  }
  function d() {
    return s(this, void 0, void 0, function* () {
      yield Promise.all([r.set([125, 0]), o.set([-125, 0])]), _();
    });
  }
  return vn(() => (d(), () => f = !0)), n.$$set = (c) => {
    "margin" in c && t(0, a = c.margin);
  }, [a, l, i, r, o];
}
class Cn extends bn {
  constructor(e) {
    super(), wn(this, e, qn, yn, pn, { margin: 0 });
  }
}
const {
  SvelteComponent: Fn,
  append: te,
  attr: X,
  binding_callbacks: tt,
  check_outros: Mt,
  create_component: Vt,
  create_slot: Ln,
  destroy_component: Nt,
  destroy_each: jt,
  detach: k,
  element: H,
  empty: de,
  ensure_array_like: ze,
  get_all_dirty_from_scope: Sn,
  get_slot_changes: zn,
  group_outros: It,
  init: Mn,
  insert: p,
  mount_component: Zt,
  noop: Ae,
  safe_not_equal: Vn,
  set_data: D,
  set_style: x,
  space: Y,
  text: L,
  toggle_class: B,
  transition_in: le,
  transition_out: ne,
  update_slot_base: Nn
} = window.__gradio__svelte__internal, { tick: jn } = window.__gradio__svelte__internal, { onDestroy: In } = window.__gradio__svelte__internal, { createEventDispatcher: Zn } = window.__gradio__svelte__internal, Bn = (n) => ({}), lt = (n) => ({});
function nt(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l[43] = t, l;
}
function it(n, e, t) {
  const l = n.slice();
  return l[41] = e[t], l;
}
function Dn(n) {
  let e, t, l, i, s = (
    /*i18n*/
    n[1]("common.error") + ""
  ), a, r, o;
  t = new ln({
    props: {
      Icon: un,
      label: (
        /*i18n*/
        n[1]("common.clear")
      ),
      disabled: !1
    }
  }), t.$on(
    "click",
    /*click_handler*/
    n[32]
  );
  const f = (
    /*#slots*/
    n[30].error
  ), u = Ln(
    f,
    n,
    /*$$scope*/
    n[29],
    lt
  );
  return {
    c() {
      e = H("div"), Vt(t.$$.fragment), l = Y(), i = H("span"), a = L(s), r = Y(), u && u.c(), X(e, "class", "clear-status svelte-1yk38uw"), X(i, "class", "error svelte-1yk38uw");
    },
    m(_, d) {
      p(_, e, d), Zt(t, e, null), p(_, l, d), p(_, i, d), te(i, a), p(_, r, d), u && u.m(_, d), o = !0;
    },
    p(_, d) {
      const c = {};
      d[0] & /*i18n*/
      2 && (c.label = /*i18n*/
      _[1]("common.clear")), t.$set(c), (!o || d[0] & /*i18n*/
      2) && s !== (s = /*i18n*/
      _[1]("common.error") + "") && D(a, s), u && u.p && (!o || d[0] & /*$$scope*/
      536870912) && Nn(
        u,
        f,
        _,
        /*$$scope*/
        _[29],
        o ? zn(
          f,
          /*$$scope*/
          _[29],
          d,
          Bn
        ) : Sn(
          /*$$scope*/
          _[29]
        ),
        lt
      );
    },
    i(_) {
      o || (le(t.$$.fragment, _), le(u, _), o = !0);
    },
    o(_) {
      ne(t.$$.fragment, _), ne(u, _), o = !1;
    },
    d(_) {
      _ && (k(e), k(l), k(i), k(r)), Nt(t), u && u.d(_);
    }
  };
}
function An(n) {
  let e, t, l, i, s, a, r, o, f, u = (
    /*variant*/
    n[8] === "default" && /*show_eta_bar*/
    n[18] && /*show_progress*/
    n[6] === "full" && st(n)
  );
  function _(m, C) {
    if (
      /*progress*/
      m[7]
    )
      return Tn;
    if (
      /*queue_position*/
      m[2] !== null && /*queue_size*/
      m[3] !== void 0 && /*queue_position*/
      m[2] >= 0
    )
      return Pn;
    if (
      /*queue_position*/
      m[2] === 0
    )
      return En;
  }
  let d = _(n), c = d && d(n), v = (
    /*timer*/
    n[5] && at(n)
  );
  const F = [On, Gn], y = [];
  function S(m, C) {
    return (
      /*last_progress_level*/
      m[15] != null ? 0 : (
        /*show_progress*/
        m[6] === "full" ? 1 : -1
      )
    );
  }
  ~(s = S(n)) && (a = y[s] = F[s](n));
  let b = !/*timer*/
  n[5] && bt(n);
  return {
    c() {
      u && u.c(), e = Y(), t = H("div"), c && c.c(), l = Y(), v && v.c(), i = Y(), a && a.c(), r = Y(), b && b.c(), o = de(), X(t, "class", "progress-text svelte-1yk38uw"), B(
        t,
        "meta-text-center",
        /*variant*/
        n[8] === "center"
      ), B(
        t,
        "meta-text",
        /*variant*/
        n[8] === "default"
      );
    },
    m(m, C) {
      u && u.m(m, C), p(m, e, C), p(m, t, C), c && c.m(t, null), te(t, l), v && v.m(t, null), p(m, i, C), ~s && y[s].m(m, C), p(m, r, C), b && b.m(m, C), p(m, o, C), f = !0;
    },
    p(m, C) {
      /*variant*/
      m[8] === "default" && /*show_eta_bar*/
      m[18] && /*show_progress*/
      m[6] === "full" ? u ? u.p(m, C) : (u = st(m), u.c(), u.m(e.parentNode, e)) : u && (u.d(1), u = null), d === (d = _(m)) && c ? c.p(m, C) : (c && c.d(1), c = d && d(m), c && (c.c(), c.m(t, l))), /*timer*/
      m[5] ? v ? v.p(m, C) : (v = at(m), v.c(), v.m(t, null)) : v && (v.d(1), v = null), (!f || C[0] & /*variant*/
      256) && B(
        t,
        "meta-text-center",
        /*variant*/
        m[8] === "center"
      ), (!f || C[0] & /*variant*/
      256) && B(
        t,
        "meta-text",
        /*variant*/
        m[8] === "default"
      );
      let M = s;
      s = S(m), s === M ? ~s && y[s].p(m, C) : (a && (It(), ne(y[M], 1, 1, () => {
        y[M] = null;
      }), Mt()), ~s ? (a = y[s], a ? a.p(m, C) : (a = y[s] = F[s](m), a.c()), le(a, 1), a.m(r.parentNode, r)) : a = null), /*timer*/
      m[5] ? b && (b.d(1), b = null) : b ? b.p(m, C) : (b = bt(m), b.c(), b.m(o.parentNode, o));
    },
    i(m) {
      f || (le(a), f = !0);
    },
    o(m) {
      ne(a), f = !1;
    },
    d(m) {
      m && (k(e), k(t), k(i), k(r), k(o)), u && u.d(m), c && c.d(), v && v.d(), ~s && y[s].d(m), b && b.d(m);
    }
  };
}
function st(n) {
  let e, t = `translateX(${/*eta_level*/
  (n[17] || 0) * 100 - 100}%)`;
  return {
    c() {
      e = H("div"), X(e, "class", "eta-bar svelte-1yk38uw"), x(e, "transform", t);
    },
    m(l, i) {
      p(l, e, i);
    },
    p(l, i) {
      i[0] & /*eta_level*/
      131072 && t !== (t = `translateX(${/*eta_level*/
      (l[17] || 0) * 100 - 100}%)`) && x(e, "transform", t);
    },
    d(l) {
      l && k(e);
    }
  };
}
function En(n) {
  let e;
  return {
    c() {
      e = L("processing |");
    },
    m(t, l) {
      p(t, e, l);
    },
    p: Ae,
    d(t) {
      t && k(e);
    }
  };
}
function Pn(n) {
  let e, t = (
    /*queue_position*/
    n[2] + 1 + ""
  ), l, i, s, a;
  return {
    c() {
      e = L("queue: "), l = L(t), i = L("/"), s = L(
        /*queue_size*/
        n[3]
      ), a = L(" |");
    },
    m(r, o) {
      p(r, e, o), p(r, l, o), p(r, i, o), p(r, s, o), p(r, a, o);
    },
    p(r, o) {
      o[0] & /*queue_position*/
      4 && t !== (t = /*queue_position*/
      r[2] + 1 + "") && D(l, t), o[0] & /*queue_size*/
      8 && D(
        s,
        /*queue_size*/
        r[3]
      );
    },
    d(r) {
      r && (k(e), k(l), k(i), k(s), k(a));
    }
  };
}
function Tn(n) {
  let e, t = ze(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = ot(it(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = de();
    },
    m(i, s) {
      for (let a = 0; a < l.length; a += 1)
        l[a] && l[a].m(i, s);
      p(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress*/
      128) {
        t = ze(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = it(i, t, a);
          l[a] ? l[a].p(r, s) : (l[a] = ot(r), l[a].c(), l[a].m(e.parentNode, e));
        }
        for (; a < l.length; a += 1)
          l[a].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), jt(l, i);
    }
  };
}
function ft(n) {
  let e, t = (
    /*p*/
    n[41].unit + ""
  ), l, i, s = " ", a;
  function r(u, _) {
    return (
      /*p*/
      u[41].length != null ? Yn : Xn
    );
  }
  let o = r(n), f = o(n);
  return {
    c() {
      f.c(), e = Y(), l = L(t), i = L(" | "), a = L(s);
    },
    m(u, _) {
      f.m(u, _), p(u, e, _), p(u, l, _), p(u, i, _), p(u, a, _);
    },
    p(u, _) {
      o === (o = r(u)) && f ? f.p(u, _) : (f.d(1), f = o(u), f && (f.c(), f.m(e.parentNode, e))), _[0] & /*progress*/
      128 && t !== (t = /*p*/
      u[41].unit + "") && D(l, t);
    },
    d(u) {
      u && (k(e), k(l), k(i), k(a)), f.d(u);
    }
  };
}
function Xn(n) {
  let e = ue(
    /*p*/
    n[41].index || 0
  ) + "", t;
  return {
    c() {
      t = L(e);
    },
    m(l, i) {
      p(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = ue(
        /*p*/
        l[41].index || 0
      ) + "") && D(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function Yn(n) {
  let e = ue(
    /*p*/
    n[41].index || 0
  ) + "", t, l, i = ue(
    /*p*/
    n[41].length
  ) + "", s;
  return {
    c() {
      t = L(e), l = L("/"), s = L(i);
    },
    m(a, r) {
      p(a, t, r), p(a, l, r), p(a, s, r);
    },
    p(a, r) {
      r[0] & /*progress*/
      128 && e !== (e = ue(
        /*p*/
        a[41].index || 0
      ) + "") && D(t, e), r[0] & /*progress*/
      128 && i !== (i = ue(
        /*p*/
        a[41].length
      ) + "") && D(s, i);
    },
    d(a) {
      a && (k(t), k(l), k(s));
    }
  };
}
function ot(n) {
  let e, t = (
    /*p*/
    n[41].index != null && ft(n)
  );
  return {
    c() {
      t && t.c(), e = de();
    },
    m(l, i) {
      t && t.m(l, i), p(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].index != null ? t ? t.p(l, i) : (t = ft(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function at(n) {
  let e, t = (
    /*eta*/
    n[0] ? `/${/*formatted_eta*/
    n[19]}` : ""
  ), l, i;
  return {
    c() {
      e = L(
        /*formatted_timer*/
        n[20]
      ), l = L(t), i = L("s");
    },
    m(s, a) {
      p(s, e, a), p(s, l, a), p(s, i, a);
    },
    p(s, a) {
      a[0] & /*formatted_timer*/
      1048576 && D(
        e,
        /*formatted_timer*/
        s[20]
      ), a[0] & /*eta, formatted_eta*/
      524289 && t !== (t = /*eta*/
      s[0] ? `/${/*formatted_eta*/
      s[19]}` : "") && D(l, t);
    },
    d(s) {
      s && (k(e), k(l), k(i));
    }
  };
}
function Gn(n) {
  let e, t;
  return e = new Cn({
    props: { margin: (
      /*variant*/
      n[8] === "default"
    ) }
  }), {
    c() {
      Vt(e.$$.fragment);
    },
    m(l, i) {
      Zt(e, l, i), t = !0;
    },
    p(l, i) {
      const s = {};
      i[0] & /*variant*/
      256 && (s.margin = /*variant*/
      l[8] === "default"), e.$set(s);
    },
    i(l) {
      t || (le(e.$$.fragment, l), t = !0);
    },
    o(l) {
      ne(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Nt(e, l);
    }
  };
}
function On(n) {
  let e, t, l, i, s, a = `${/*last_progress_level*/
  n[15] * 100}%`, r = (
    /*progress*/
    n[7] != null && rt(n)
  );
  return {
    c() {
      e = H("div"), t = H("div"), r && r.c(), l = Y(), i = H("div"), s = H("div"), X(t, "class", "progress-level-inner svelte-1yk38uw"), X(s, "class", "progress-bar svelte-1yk38uw"), x(s, "width", a), X(i, "class", "progress-bar-wrap svelte-1yk38uw"), X(e, "class", "progress-level svelte-1yk38uw");
    },
    m(o, f) {
      p(o, e, f), te(e, t), r && r.m(t, null), te(e, l), te(e, i), te(i, s), n[31](s);
    },
    p(o, f) {
      /*progress*/
      o[7] != null ? r ? r.p(o, f) : (r = rt(o), r.c(), r.m(t, null)) : r && (r.d(1), r = null), f[0] & /*last_progress_level*/
      32768 && a !== (a = `${/*last_progress_level*/
      o[15] * 100}%`) && x(s, "width", a);
    },
    i: Ae,
    o: Ae,
    d(o) {
      o && k(e), r && r.d(), n[31](null);
    }
  };
}
function rt(n) {
  let e, t = ze(
    /*progress*/
    n[7]
  ), l = [];
  for (let i = 0; i < t.length; i += 1)
    l[i] = mt(nt(n, t, i));
  return {
    c() {
      for (let i = 0; i < l.length; i += 1)
        l[i].c();
      e = de();
    },
    m(i, s) {
      for (let a = 0; a < l.length; a += 1)
        l[a] && l[a].m(i, s);
      p(i, e, s);
    },
    p(i, s) {
      if (s[0] & /*progress_level, progress*/
      16512) {
        t = ze(
          /*progress*/
          i[7]
        );
        let a;
        for (a = 0; a < t.length; a += 1) {
          const r = nt(i, t, a);
          l[a] ? l[a].p(r, s) : (l[a] = mt(r), l[a].c(), l[a].m(e.parentNode, e));
        }
        for (; a < l.length; a += 1)
          l[a].d(1);
        l.length = t.length;
      }
    },
    d(i) {
      i && k(e), jt(l, i);
    }
  };
}
function ut(n) {
  let e, t, l, i, s = (
    /*i*/
    n[43] !== 0 && Rn()
  ), a = (
    /*p*/
    n[41].desc != null && _t(n)
  ), r = (
    /*p*/
    n[41].desc != null && /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null && ct()
  ), o = (
    /*progress_level*/
    n[14] != null && dt(n)
  );
  return {
    c() {
      s && s.c(), e = Y(), a && a.c(), t = Y(), r && r.c(), l = Y(), o && o.c(), i = de();
    },
    m(f, u) {
      s && s.m(f, u), p(f, e, u), a && a.m(f, u), p(f, t, u), r && r.m(f, u), p(f, l, u), o && o.m(f, u), p(f, i, u);
    },
    p(f, u) {
      /*p*/
      f[41].desc != null ? a ? a.p(f, u) : (a = _t(f), a.c(), a.m(t.parentNode, t)) : a && (a.d(1), a = null), /*p*/
      f[41].desc != null && /*progress_level*/
      f[14] && /*progress_level*/
      f[14][
        /*i*/
        f[43]
      ] != null ? r || (r = ct(), r.c(), r.m(l.parentNode, l)) : r && (r.d(1), r = null), /*progress_level*/
      f[14] != null ? o ? o.p(f, u) : (o = dt(f), o.c(), o.m(i.parentNode, i)) : o && (o.d(1), o = null);
    },
    d(f) {
      f && (k(e), k(t), k(l), k(i)), s && s.d(f), a && a.d(f), r && r.d(f), o && o.d(f);
    }
  };
}
function Rn(n) {
  let e;
  return {
    c() {
      e = L(" /");
    },
    m(t, l) {
      p(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function _t(n) {
  let e = (
    /*p*/
    n[41].desc + ""
  ), t;
  return {
    c() {
      t = L(e);
    },
    m(l, i) {
      p(l, t, i);
    },
    p(l, i) {
      i[0] & /*progress*/
      128 && e !== (e = /*p*/
      l[41].desc + "") && D(t, e);
    },
    d(l) {
      l && k(t);
    }
  };
}
function ct(n) {
  let e;
  return {
    c() {
      e = L("-");
    },
    m(t, l) {
      p(t, e, l);
    },
    d(t) {
      t && k(e);
    }
  };
}
function dt(n) {
  let e = (100 * /*progress_level*/
  (n[14][
    /*i*/
    n[43]
  ] || 0)).toFixed(1) + "", t, l;
  return {
    c() {
      t = L(e), l = L("%");
    },
    m(i, s) {
      p(i, t, s), p(i, l, s);
    },
    p(i, s) {
      s[0] & /*progress_level*/
      16384 && e !== (e = (100 * /*progress_level*/
      (i[14][
        /*i*/
        i[43]
      ] || 0)).toFixed(1) + "") && D(t, e);
    },
    d(i) {
      i && (k(t), k(l));
    }
  };
}
function mt(n) {
  let e, t = (
    /*p*/
    (n[41].desc != null || /*progress_level*/
    n[14] && /*progress_level*/
    n[14][
      /*i*/
      n[43]
    ] != null) && ut(n)
  );
  return {
    c() {
      t && t.c(), e = de();
    },
    m(l, i) {
      t && t.m(l, i), p(l, e, i);
    },
    p(l, i) {
      /*p*/
      l[41].desc != null || /*progress_level*/
      l[14] && /*progress_level*/
      l[14][
        /*i*/
        l[43]
      ] != null ? t ? t.p(l, i) : (t = ut(l), t.c(), t.m(e.parentNode, e)) : t && (t.d(1), t = null);
    },
    d(l) {
      l && k(e), t && t.d(l);
    }
  };
}
function bt(n) {
  let e, t;
  return {
    c() {
      e = H("p"), t = L(
        /*loading_text*/
        n[9]
      ), X(e, "class", "loading svelte-1yk38uw");
    },
    m(l, i) {
      p(l, e, i), te(e, t);
    },
    p(l, i) {
      i[0] & /*loading_text*/
      512 && D(
        t,
        /*loading_text*/
        l[9]
      );
    },
    d(l) {
      l && k(e);
    }
  };
}
function Hn(n) {
  let e, t, l, i, s;
  const a = [An, Dn], r = [];
  function o(f, u) {
    return (
      /*status*/
      f[4] === "pending" ? 0 : (
        /*status*/
        f[4] === "error" ? 1 : -1
      )
    );
  }
  return ~(t = o(n)) && (l = r[t] = a[t](n)), {
    c() {
      e = H("div"), l && l.c(), X(e, "class", i = "wrap " + /*variant*/
      n[8] + " " + /*show_progress*/
      n[6] + " svelte-1yk38uw"), B(e, "hide", !/*status*/
      n[4] || /*status*/
      n[4] === "complete" || /*show_progress*/
      n[6] === "hidden"), B(
        e,
        "translucent",
        /*variant*/
        n[8] === "center" && /*status*/
        (n[4] === "pending" || /*status*/
        n[4] === "error") || /*translucent*/
        n[11] || /*show_progress*/
        n[6] === "minimal"
      ), B(
        e,
        "generating",
        /*status*/
        n[4] === "generating"
      ), B(
        e,
        "border",
        /*border*/
        n[12]
      ), x(
        e,
        "position",
        /*absolute*/
        n[10] ? "absolute" : "static"
      ), x(
        e,
        "padding",
        /*absolute*/
        n[10] ? "0" : "var(--size-8) 0"
      );
    },
    m(f, u) {
      p(f, e, u), ~t && r[t].m(e, null), n[33](e), s = !0;
    },
    p(f, u) {
      let _ = t;
      t = o(f), t === _ ? ~t && r[t].p(f, u) : (l && (It(), ne(r[_], 1, 1, () => {
        r[_] = null;
      }), Mt()), ~t ? (l = r[t], l ? l.p(f, u) : (l = r[t] = a[t](f), l.c()), le(l, 1), l.m(e, null)) : l = null), (!s || u[0] & /*variant, show_progress*/
      320 && i !== (i = "wrap " + /*variant*/
      f[8] + " " + /*show_progress*/
      f[6] + " svelte-1yk38uw")) && X(e, "class", i), (!s || u[0] & /*variant, show_progress, status, show_progress*/
      336) && B(e, "hide", !/*status*/
      f[4] || /*status*/
      f[4] === "complete" || /*show_progress*/
      f[6] === "hidden"), (!s || u[0] & /*variant, show_progress, variant, status, translucent, show_progress*/
      2384) && B(
        e,
        "translucent",
        /*variant*/
        f[8] === "center" && /*status*/
        (f[4] === "pending" || /*status*/
        f[4] === "error") || /*translucent*/
        f[11] || /*show_progress*/
        f[6] === "minimal"
      ), (!s || u[0] & /*variant, show_progress, status*/
      336) && B(
        e,
        "generating",
        /*status*/
        f[4] === "generating"
      ), (!s || u[0] & /*variant, show_progress, border*/
      4416) && B(
        e,
        "border",
        /*border*/
        f[12]
      ), u[0] & /*absolute*/
      1024 && x(
        e,
        "position",
        /*absolute*/
        f[10] ? "absolute" : "static"
      ), u[0] & /*absolute*/
      1024 && x(
        e,
        "padding",
        /*absolute*/
        f[10] ? "0" : "var(--size-8) 0"
      );
    },
    i(f) {
      s || (le(l), s = !0);
    },
    o(f) {
      ne(l), s = !1;
    },
    d(f) {
      f && k(e), ~t && r[t].d(), n[33](null);
    }
  };
}
var Jn = function(n, e, t, l) {
  function i(s) {
    return s instanceof t ? s : new t(function(a) {
      a(s);
    });
  }
  return new (t || (t = Promise))(function(s, a) {
    function r(u) {
      try {
        f(l.next(u));
      } catch (_) {
        a(_);
      }
    }
    function o(u) {
      try {
        f(l.throw(u));
      } catch (_) {
        a(_);
      }
    }
    function f(u) {
      u.done ? s(u.value) : i(u.value).then(r, o);
    }
    f((l = l.apply(n, e || [])).next());
  });
};
let qe = [], Ie = !1;
function Kn(n) {
  return Jn(this, arguments, void 0, function* (e, t = !0) {
    if (!(window.__gradio_mode__ === "website" || window.__gradio_mode__ !== "app" && t !== !0)) {
      if (qe.push(e), !Ie)
        Ie = !0;
      else
        return;
      yield jn(), requestAnimationFrame(() => {
        let l = [0, 0];
        for (let i = 0; i < qe.length; i++) {
          const a = qe[i].getBoundingClientRect();
          (i === 0 || a.top + window.scrollY <= l[0]) && (l[0] = a.top + window.scrollY, l[1] = i);
        }
        window.scrollTo({ top: l[0] - 20, behavior: "smooth" }), Ie = !1, qe = [];
      });
    }
  });
}
function Qn(n, e, t) {
  let l, { $$slots: i = {}, $$scope: s } = e;
  this && this.__awaiter;
  const a = Zn();
  let { i18n: r } = e, { eta: o = null } = e, { queue_position: f } = e, { queue_size: u } = e, { status: _ } = e, { scroll_to_output: d = !1 } = e, { timer: c = !0 } = e, { show_progress: v = "full" } = e, { message: F = null } = e, { progress: y = null } = e, { variant: S = "default" } = e, { loading_text: b = "Loading..." } = e, { absolute: m = !0 } = e, { translucent: C = !1 } = e, { border: M = !1 } = e, { autoscroll: g } = e, z, w = !1, ie = 0, I = 0, A = null, Q = null, U = 0, Z = null, $, G = null, se = !0;
  const J = () => {
    t(0, o = t(27, A = t(19, ge = null))), t(25, ie = performance.now()), t(26, I = 0), w = !0, fe();
  };
  function fe() {
    requestAnimationFrame(() => {
      t(26, I = (performance.now() - ie) / 1e3), w && fe();
    });
  }
  function Ge() {
    t(26, I = 0), t(0, o = t(27, A = t(19, ge = null))), w && (w = !1);
  }
  In(() => {
    w && Ge();
  });
  let ge = null;
  function Bt(h) {
    tt[h ? "unshift" : "push"](() => {
      G = h, t(16, G), t(7, y), t(14, Z), t(15, $);
    });
  }
  const Dt = () => {
    a("clear_status");
  };
  function At(h) {
    tt[h ? "unshift" : "push"](() => {
      z = h, t(13, z);
    });
  }
  return n.$$set = (h) => {
    "i18n" in h && t(1, r = h.i18n), "eta" in h && t(0, o = h.eta), "queue_position" in h && t(2, f = h.queue_position), "queue_size" in h && t(3, u = h.queue_size), "status" in h && t(4, _ = h.status), "scroll_to_output" in h && t(22, d = h.scroll_to_output), "timer" in h && t(5, c = h.timer), "show_progress" in h && t(6, v = h.show_progress), "message" in h && t(23, F = h.message), "progress" in h && t(7, y = h.progress), "variant" in h && t(8, S = h.variant), "loading_text" in h && t(9, b = h.loading_text), "absolute" in h && t(10, m = h.absolute), "translucent" in h && t(11, C = h.translucent), "border" in h && t(12, M = h.border), "autoscroll" in h && t(24, g = h.autoscroll), "$$scope" in h && t(29, s = h.$$scope);
  }, n.$$.update = () => {
    n.$$.dirty[0] & /*eta, old_eta, timer_start, eta_from_start*/
    436207617 && (o === null && t(0, o = A), o != null && A !== o && (t(28, Q = (performance.now() - ie) / 1e3 + o), t(19, ge = Q.toFixed(1)), t(27, A = o))), n.$$.dirty[0] & /*eta_from_start, timer_diff*/
    335544320 && t(17, U = Q === null || Q <= 0 || !I ? null : Math.min(I / Q, 1)), n.$$.dirty[0] & /*progress*/
    128 && y != null && t(18, se = !1), n.$$.dirty[0] & /*progress, progress_level, progress_bar, last_progress_level*/
    114816 && (y != null ? t(14, Z = y.map((h) => {
      if (h.index != null && h.length != null)
        return h.index / h.length;
      if (h.progress != null)
        return h.progress;
    })) : t(14, Z = null), Z ? (t(15, $ = Z[Z.length - 1]), G && ($ === 0 ? t(16, G.style.transition = "0", G) : t(16, G.style.transition = "150ms", G))) : t(15, $ = void 0)), n.$$.dirty[0] & /*status*/
    16 && (_ === "pending" ? J() : Ge()), n.$$.dirty[0] & /*el, scroll_to_output, status, autoscroll*/
    20979728 && z && d && (_ === "pending" || _ === "complete") && Kn(z, g), n.$$.dirty[0] & /*status, message*/
    8388624, n.$$.dirty[0] & /*timer_diff*/
    67108864 && t(20, l = I.toFixed(1));
  }, [
    o,
    r,
    f,
    u,
    _,
    c,
    v,
    y,
    S,
    b,
    m,
    C,
    M,
    z,
    Z,
    $,
    G,
    U,
    se,
    ge,
    l,
    a,
    d,
    F,
    g,
    ie,
    I,
    A,
    Q,
    s,
    i,
    Bt,
    Dt,
    At
  ];
}
class Un extends Fn {
  constructor(e) {
    super(), Mn(
      this,
      e,
      Qn,
      Hn,
      Vn,
      {
        i18n: 1,
        eta: 0,
        queue_position: 2,
        queue_size: 3,
        status: 4,
        scroll_to_output: 22,
        timer: 5,
        show_progress: 6,
        message: 23,
        progress: 7,
        variant: 8,
        loading_text: 9,
        absolute: 10,
        translucent: 11,
        border: 12,
        autoscroll: 24
      },
      null,
      [-1, -1]
    );
  }
}
const {
  SvelteComponent: Wn,
  append: ht,
  assign: xn,
  attr: W,
  binding_callbacks: $n,
  check_outros: ei,
  create_component: Te,
  destroy_component: Xe,
  detach: Ee,
  element: gt,
  flush: N,
  get_spread_object: ti,
  get_spread_update: li,
  group_outros: ni,
  init: ii,
  insert: Pe,
  listen: wt,
  mount_component: Ye,
  run_all: si,
  safe_not_equal: fi,
  set_data: oi,
  set_input_value: kt,
  space: pt,
  text: ai,
  toggle_class: ri,
  transition_in: _e,
  transition_out: he
} = window.__gradio__svelte__internal, { tick: ui } = window.__gradio__svelte__internal;
function vt(n) {
  let e, t;
  const l = [
    { autoscroll: (
      /*gradio*/
      n[1].autoscroll
    ) },
    { i18n: (
      /*gradio*/
      n[1].i18n
    ) },
    /*loading_status*/
    n[10]
  ];
  let i = {};
  for (let s = 0; s < l.length; s += 1)
    i = xn(i, l[s]);
  return e = new Un({ props: i }), e.$on(
    "clear_status",
    /*clear_status_handler*/
    n[16]
  ), {
    c() {
      Te(e.$$.fragment);
    },
    m(s, a) {
      Ye(e, s, a), t = !0;
    },
    p(s, a) {
      const r = a & /*gradio, loading_status*/
      1026 ? li(l, [
        a & /*gradio*/
        2 && { autoscroll: (
          /*gradio*/
          s[1].autoscroll
        ) },
        a & /*gradio*/
        2 && { i18n: (
          /*gradio*/
          s[1].i18n
        ) },
        a & /*loading_status*/
        1024 && ti(
          /*loading_status*/
          s[10]
        )
      ]) : {};
      e.$set(r);
    },
    i(s) {
      t || (_e(e.$$.fragment, s), t = !0);
    },
    o(s) {
      he(e.$$.fragment, s), t = !1;
    },
    d(s) {
      Xe(e, s);
    }
  };
}
function _i(n) {
  let e;
  return {
    c() {
      e = ai(
        /*label*/
        n[2]
      );
    },
    m(t, l) {
      Pe(t, e, l);
    },
    p(t, l) {
      l & /*label*/
      4 && oi(
        e,
        /*label*/
        t[2]
      );
    },
    d(t) {
      t && Ee(e);
    }
  };
}
function ci(n) {
  let e, t, l, i, s, a, r, o, f, u, _ = (
    /*loading_status*/
    n[10] && vt(n)
  );
  return l = new Tl({
    props: {
      show_label: (
        /*show_label*/
        n[7]
      ),
      info: void 0,
      $$slots: { default: [_i] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      _ && _.c(), e = pt(), t = gt("label"), Te(l.$$.fragment), i = pt(), s = gt("input"), W(s, "data-testid", "textbox"), W(s, "type", "text"), W(s, "class", "scroll-hide svelte-2jrh70"), W(
        s,
        "placeholder",
        /*placeholder*/
        n[6]
      ), s.disabled = a = !/*interactive*/
      n[11], W(s, "dir", r = /*rtl*/
      n[12] ? "rtl" : "ltr"), W(t, "class", "svelte-2jrh70"), ri(t, "container", mi);
    },
    m(d, c) {
      _ && _.m(d, c), Pe(d, e, c), Pe(d, t, c), Ye(l, t, null), ht(t, i), ht(t, s), kt(
        s,
        /*value*/
        n[0]
      ), n[18](s), o = !0, f || (u = [
        wt(
          s,
          "input",
          /*input_input_handler*/
          n[17]
        ),
        wt(
          s,
          "keypress",
          /*handle_keypress*/
          n[14]
        )
      ], f = !0);
    },
    p(d, c) {
      /*loading_status*/
      d[10] ? _ ? (_.p(d, c), c & /*loading_status*/
      1024 && _e(_, 1)) : (_ = vt(d), _.c(), _e(_, 1), _.m(e.parentNode, e)) : _ && (ni(), he(_, 1, 1, () => {
        _ = null;
      }), ei());
      const v = {};
      c & /*show_label*/
      128 && (v.show_label = /*show_label*/
      d[7]), c & /*$$scope, label*/
      2097156 && (v.$$scope = { dirty: c, ctx: d }), l.$set(v), (!o || c & /*placeholder*/
      64) && W(
        s,
        "placeholder",
        /*placeholder*/
        d[6]
      ), (!o || c & /*interactive*/
      2048 && a !== (a = !/*interactive*/
      d[11])) && (s.disabled = a), (!o || c & /*rtl*/
      4096 && r !== (r = /*rtl*/
      d[12] ? "rtl" : "ltr")) && W(s, "dir", r), c & /*value*/
      1 && s.value !== /*value*/
      d[0] && kt(
        s,
        /*value*/
        d[0]
      );
    },
    i(d) {
      o || (_e(_), _e(l.$$.fragment, d), o = !0);
    },
    o(d) {
      he(_), he(l.$$.fragment, d), o = !1;
    },
    d(d) {
      d && (Ee(e), Ee(t)), _ && _.d(d), Xe(l), n[18](null), f = !1, si(u);
    }
  };
}
function di(n) {
  let e, t;
  return e = new nl({
    props: {
      visible: (
        /*visible*/
        n[5]
      ),
      elem_id: (
        /*elem_id*/
        n[3]
      ),
      elem_classes: (
        /*elem_classes*/
        n[4]
      ),
      scale: (
        /*scale*/
        n[8]
      ),
      min_width: (
        /*min_width*/
        n[9]
      ),
      allow_overflow: !1,
      padding: !0,
      $$slots: { default: [ci] },
      $$scope: { ctx: n }
    }
  }), {
    c() {
      Te(e.$$.fragment);
    },
    m(l, i) {
      Ye(e, l, i), t = !0;
    },
    p(l, [i]) {
      const s = {};
      i & /*visible*/
      32 && (s.visible = /*visible*/
      l[5]), i & /*elem_id*/
      8 && (s.elem_id = /*elem_id*/
      l[3]), i & /*elem_classes*/
      16 && (s.elem_classes = /*elem_classes*/
      l[4]), i & /*scale*/
      256 && (s.scale = /*scale*/
      l[8]), i & /*min_width*/
      512 && (s.min_width = /*min_width*/
      l[9]), i & /*$$scope, placeholder, interactive, rtl, value, el, show_label, label, gradio, loading_status*/
      2112711 && (s.$$scope = { dirty: i, ctx: l }), e.$set(s);
    },
    i(l) {
      t || (_e(e.$$.fragment, l), t = !0);
    },
    o(l) {
      he(e.$$.fragment, l), t = !1;
    },
    d(l) {
      Xe(e, l);
    }
  };
}
const mi = !0;
function bi(n, e, t) {
  var l = this && this.__awaiter || function(w, ie, I, A) {
    function Q(U) {
      return U instanceof I ? U : new I(function(Z) {
        Z(U);
      });
    }
    return new (I || (I = Promise))(function(U, Z) {
      function $(J) {
        try {
          se(A.next(J));
        } catch (fe) {
          Z(fe);
        }
      }
      function G(J) {
        try {
          se(A.throw(J));
        } catch (fe) {
          Z(fe);
        }
      }
      function se(J) {
        J.done ? U(J.value) : Q(J.value).then($, G);
      }
      se((A = A.apply(w, ie || [])).next());
    });
  };
  let { gradio: i } = e, { label: s = "Textbox" } = e, { elem_id: a = "" } = e, { elem_classes: r = [] } = e, { visible: o = !0 } = e, { value: f = "" } = e, { placeholder: u = "" } = e, { show_label: _ } = e, { scale: d = null } = e, { min_width: c = void 0 } = e, { loading_status: v = void 0 } = e, { value_is_output: F = !1 } = e, { interactive: y } = e, { rtl: S = !1 } = e, b;
  function m() {
    i.dispatch("change"), F || i.dispatch("input");
  }
  function C(w) {
    return l(this, void 0, void 0, function* () {
      yield ui(), w.key === "Enter" && (w.preventDefault(), i.dispatch("submit"));
    });
  }
  const M = () => i.dispatch("clear_status", v);
  function g() {
    f = this.value, t(0, f);
  }
  function z(w) {
    $n[w ? "unshift" : "push"](() => {
      b = w, t(13, b);
    });
  }
  return n.$$set = (w) => {
    "gradio" in w && t(1, i = w.gradio), "label" in w && t(2, s = w.label), "elem_id" in w && t(3, a = w.elem_id), "elem_classes" in w && t(4, r = w.elem_classes), "visible" in w && t(5, o = w.visible), "value" in w && t(0, f = w.value), "placeholder" in w && t(6, u = w.placeholder), "show_label" in w && t(7, _ = w.show_label), "scale" in w && t(8, d = w.scale), "min_width" in w && t(9, c = w.min_width), "loading_status" in w && t(10, v = w.loading_status), "value_is_output" in w && t(15, F = w.value_is_output), "interactive" in w && t(11, y = w.interactive), "rtl" in w && t(12, S = w.rtl);
  }, n.$$.update = () => {
    n.$$.dirty & /*value*/
    1 && f === null && t(0, f = ""), n.$$.dirty & /*value*/
    1 && m();
  }, [
    f,
    i,
    s,
    a,
    r,
    o,
    u,
    _,
    d,
    c,
    v,
    y,
    S,
    b,
    C,
    F,
    M,
    g,
    z
  ];
}
class hi extends Wn {
  constructor(e) {
    super(), ii(this, e, bi, di, fi, {
      gradio: 1,
      label: 2,
      elem_id: 3,
      elem_classes: 4,
      visible: 5,
      value: 0,
      placeholder: 6,
      show_label: 7,
      scale: 8,
      min_width: 9,
      loading_status: 10,
      value_is_output: 15,
      interactive: 11,
      rtl: 12
    });
  }
  get gradio() {
    return this.$$.ctx[1];
  }
  set gradio(e) {
    this.$$set({ gradio: e }), N();
  }
  get label() {
    return this.$$.ctx[2];
  }
  set label(e) {
    this.$$set({ label: e }), N();
  }
  get elem_id() {
    return this.$$.ctx[3];
  }
  set elem_id(e) {
    this.$$set({ elem_id: e }), N();
  }
  get elem_classes() {
    return this.$$.ctx[4];
  }
  set elem_classes(e) {
    this.$$set({ elem_classes: e }), N();
  }
  get visible() {
    return this.$$.ctx[5];
  }
  set visible(e) {
    this.$$set({ visible: e }), N();
  }
  get value() {
    return this.$$.ctx[0];
  }
  set value(e) {
    this.$$set({ value: e }), N();
  }
  get placeholder() {
    return this.$$.ctx[6];
  }
  set placeholder(e) {
    this.$$set({ placeholder: e }), N();
  }
  get show_label() {
    return this.$$.ctx[7];
  }
  set show_label(e) {
    this.$$set({ show_label: e }), N();
  }
  get scale() {
    return this.$$.ctx[8];
  }
  set scale(e) {
    this.$$set({ scale: e }), N();
  }
  get min_width() {
    return this.$$.ctx[9];
  }
  set min_width(e) {
    this.$$set({ min_width: e }), N();
  }
  get loading_status() {
    return this.$$.ctx[10];
  }
  set loading_status(e) {
    this.$$set({ loading_status: e }), N();
  }
  get value_is_output() {
    return this.$$.ctx[15];
  }
  set value_is_output(e) {
    this.$$set({ value_is_output: e }), N();
  }
  get interactive() {
    return this.$$.ctx[11];
  }
  set interactive(e) {
    this.$$set({ interactive: e }), N();
  }
  get rtl() {
    return this.$$.ctx[12];
  }
  set rtl(e) {
    this.$$set({ rtl: e }), N();
  }
}
export {
  hi as default
};
