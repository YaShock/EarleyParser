from . import semantics
dict = {}
def create():
    dict[2661411879960] = (semantics.expr_enter, semantics.expr_exit)
    dict[2661411880408] = (semantics.sum_enter, semantics.sum_exit)
    dict[2661411880464] = (semantics.sum_unary_enter, semantics.sum_unary_exit)
    dict[2661411880744] = (semantics.product_enter, semantics.product_exit)
    dict[2661411880800] = (semantics.product_unary_enter, semantics.product_unary_exit)
    dict[2661411934560] = (semantics.parentheses_enter, semantics.parentheses_exit)
    dict[2661411934672] = (semantics.num_factor_enter, semantics.num_factor_exit)
    dict[2661411934952] = (semantics.number_enter, semantics.number_exit)
    dict[2661411935064] = (semantics.number_digit_enter, semantics.number_digit_exit)
    dict[2661411935400] = (semantics.digit_enter, semantics.digit_exit)
    dict[2661411935680] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[2661411935960] = (semantics.operator_expr_enter, semantics.operator_expr_exit)
    dict[2661411936128] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
    dict[2661411936408] = (semantics.operator_prod_enter, semantics.operator_prod_exit)
