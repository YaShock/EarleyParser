from . import semantics
dict = {}
def create():
    dict[140515602270416] = (semantics.expr_enter, semantics.expr_exit)
    dict[140515602270920] = (semantics.sum_enter, semantics.sum_exit)
    dict[140515602270976] = (semantics.sum_unary_enter, semantics.sum_unary_exit)
    dict[140515602271256] = (semantics.product_enter, semantics.product_exit)
    dict[140515602271312] = (semantics.product_unary_enter, semantics.product_unary_exit)
    dict[140515602271760] = (semantics.parentheses_enter, semantics.parentheses_exit)
    dict[140515602271872] = (semantics.num_factor_enter, semantics.num_factor_exit)
    dict[140515602272152] = (semantics.number_enter, semantics.number_exit)
    dict[140515602292808] = (semantics.number_digit_enter, semantics.number_digit_exit)
    dict[140515602293144] = (semantics.digit_enter, semantics.digit_exit)
    dict[140515602293424] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[140515602293704] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[140515602293872] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
    dict[140515602294152] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
