/**
 * @id java-kotlin/cast
 * @name Cast
 * @description Cast
 * @kind problem
 * @problem.severity recommendation
 */

import java

from CastingExpr c
where c.getTypeExpr().getType() instanceof RefType
select c, c.getEnclosingCallable().getQualifiedName() + " " + ((RefType) c.getTypeExpr().getType()).getQualifiedName()