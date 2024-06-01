/**
 * @id java-kotlin/create
 * @name Create
 * @description Create
 * @kind problem
 * @problem.severity recommendation
 */

import java

from Call c
where c.getCallee() instanceof Constructor
select c, c.getCaller().getQualifiedName() + " "
    + ((Constructor) c.getCallee()).getDeclaringType().getQualifiedName()