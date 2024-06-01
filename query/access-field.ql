/**
 * @id java-kotlin/access-field
 * @name Use
 * @description Use (access-field)
 * @kind problem
 * @problem.severity recommendation
 */

import java

from FieldAccess acc
select acc, acc.getSite().getQualifiedName() + " " + acc.getField().getQualifiedName()