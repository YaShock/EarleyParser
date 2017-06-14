from . import semantics
dict = {}
def create():
    dict[1830208306144] = (semantics.expr_enter, semantics.expr_exit)
    dict[1830208306592] = (semantics.sum_enter, semantics.sum_exit)
    dict[1830208306648] = (semantics.sum_unary_enter, semantics.sum_unary_exit)
    dict[1830208306928] = (semantics.product_enter, semantics.product_exit)
    dict[1830208306984] = (semantics.product_unary_enter, semantics.product_unary_exit)
    dict[1830208360744] = (semantics.parentheses_enter, semantics.parentheses_exit)
    dict[1830208360856] = (semantics.num_factor_enter, semantics.num_factor_exit)
    dict[1830208361024] = (semantics.number_enter, semantics.number_exit)
    dict[1830208361416] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[1830208361696] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[1830208361864] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
    dict[1830208362144] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
