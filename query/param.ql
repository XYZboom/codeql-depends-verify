/**
 * @id java-kotlin/param
 * @name Parameter
 * @description Parameter
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Callable c, RefType t
where c.getAParamType() = t
select c, c.getQualifiedName() + " " + t.getQualifiedName()